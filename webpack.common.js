/* global __dirname */
const path = require('path');

module.exports = {
    entry: {
        learning: './frontend/src/learning/index.js',
        assignment: './frontend/src/assignment/index.js'
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'static/scripts')
    },
    resolve: {
        extensions: ['.ts', '.tsx', '.js']
    },
    module: {
        rules: [
            {
                test: /\.(js|ts)$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                options: {
                    presets: [
                        '@babel/preset-env',
                        '@babel/react',{
                            'plugins': ['@babel/plugin-proposal-class-properties']
                        },
                        '@babel/preset-typescript'
                    ],
                }
            },
            {
                test: /\.css$/,
                use: ['styles-loader', 'css-loader'],
                exclude: /node_modules/
            }
        ]
    },

    devServer: {
        contentBase : path.join (__dirname,'public'),
        historyApiFallback : true
    },
      
    devtool: 'source-map'
};