/* global __dirname */
const path = require('path');

module.exports = {
    entry: {
        learning: './frontend/learning/index.tsx',
        assignment: './frontend/assignment/index.tsx'
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
                test: /\.(js|ts|tsx)$/,
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
                use: ['style-loader', 'css-loader'],
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