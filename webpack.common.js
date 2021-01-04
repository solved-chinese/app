/* global __dirname */
const path = require('path');

module.exports = {
    entry: {
        learning: './frontend/src/learning/index.js'
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'static/scripts')
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                options: {
                    presets: ['@babel/preset-env',
                        '@babel/react',{
                            'plugins': ['@babel/plugin-proposal-class-properties']}]
                }
            }
        ]
    },

    devServer: {
        contentBase : path.join (__dirname,'public'),
        historyApiFallback : true
    },
      
    devtool: 'source-map'
};