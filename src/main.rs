//! EKFを用いた姿勢推定アルゴリズムを実装
//! 
//! 参考：田原 誠, 鈴木 智, 野波 健蔵, ”小型軽量汎用性を特徴とする小型姿勢センサの開発”, 
//! 　　　日本機械学会論文集(C編), Vol. 77, No. 781, 2011.

use std::fs;
use std::io::{Write, BufWriter};
use rand::distributions::{Distribution, Normal};
use quaternion as quat;

mod ahrs;

const DT: f64 = 0.05;  // AHRS側でもこの定数を使っている
const SIM_TIME: f64 = 100.0;
const N: usize = (SIM_TIME / DT) as usize + 1;

fn main() {
    // CSVファイルにデータ保存
    // 同一ファイルが存在したら上書き
    let mut file = BufWriter::new( fs::File::create("result.csv").unwrap() );

    // 標準正規分布の乱数を生成
    let randn = Normal::new(0.0, 1.0);  // 平均値:0，標準偏差:1

    // 誤差共分散行列の初期値
    let mut p = [[0.0; 10]; 10];
    for i in 0..10 {
        p[i][i] = 1000.0;
    }

    // 入力行列
    let mut g = [[0.0; 3]; 10];
    for i in 0..3 {
        g[i+4][i] = DT;
    }

    // システムノイズの共分散行列
    let mut q = [[0.0; 3]; 3];
    for i in 0..3 {
        q[i][i] = 0.001;
    }
    // 観測ノイズの分散（共分散行列の対角成分）
    let mut r = [0.0; 6];
    for i in 0..3 {
        r[i] = 0.3;
        r[i+3] = 0.2;
    }

    let mut attitude_filter = ahrs::ExUdFilter::new(p, g, q, r);
    attitude_filter.x[0] = 1.0;  // 初期値は恒等四元数

    let mut x = attitude_filter.x;
    let mut y_true = ahrs::calc_h(x);
    let mut y = y_true;
    for i in 0..y.len(){
        y[i] += randn.sample(&mut rand::thread_rng()) * r[i].sqrt();
    }

    // ---- Loop start ---- //
    let gyr = [0.1; 3];
    for t in 1..N {

        if t > N/2 && t<3*N/4 {
            x[8] = 2.0;
            //x[9] = 2.0;
            //gyr = [0.01, 0.0, 0.05];
        } else {
            x[8] = 0.0;
        }

        x = ahrs::calc_f(x, gyr);
        y_true = ahrs::calc_h(x);
        for i in 0..y.len() {
            y[i] = y_true[i] + randn.sample(&mut rand::thread_rng()) * r[i].sqrt();
        }

        attitude_filter.predict(gyr);
        attitude_filter.filtering(&y_true);

        // ---------- データ書き込み ---------- //
        // 時刻
        file.write( format!("{:.3},", t as f64 * DT ).as_bytes() ).unwrap();
        // 出力の真値
        for i in 0..6 {
            file.write( format!("{:.7},", y_true[i] ).as_bytes() ).unwrap();
        }
        // 出力の観測値
        for i in 0..6 {
            file.write( format!("{:.7},", y[i] ).as_bytes() ).unwrap();
        }
        // オイラー角の真値
        let ypr_true = quat::to_euler_angles((x[0], [x[1], x[2], x[3]]));
        for i in 0..3 {
            file.write( format!("{:.7},", ypr_true[i] ).as_bytes() ).unwrap();
        }
        // オイラー角の推定値
        let ypr_hat = quat::to_euler_angles((attitude_filter.x[0], [attitude_filter.x[1], attitude_filter.x[2], attitude_filter.x[3]]));
        for i in 0..3 {
            file.write( format!("{:.7},", ypr_hat[i] ).as_bytes() ).unwrap();
        }
        // 状態変数の真値
        for i in 0..10 {
            file.write( format!("{:.7},", x[i] ).as_bytes() ).unwrap();
        }
        // 推定した状態変数
        for i in 0..10 {
            file.write( format!("{:.7}", attitude_filter.x[i] ).as_bytes() ).unwrap();
            if i < 9 {
                file.write( ",".as_bytes() ).unwrap();
            } else {
                file.write( "\n".as_bytes() ).unwrap();
            }
        }
        // ------------------------------------ //
    }
}