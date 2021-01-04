const { ESLint } = require("eslint");

module.exports = {
    'env': {
        'browser': true,
        'es2021': true,
        'amd': true
    },
    'globals': {
        'window': true,
        'module': true
    },
    'extends': [
        'eslint:recommended',
        'plugin:react/recommended'
    ],
    'parser': 'babel-eslint',
    'parserOptions': {
        'ecmaFeatures': {
            'jsx': true
        },
        'ecmaVersion': 12,
        'sourceType': 'module'
    },
    'settings': {
        'import/resolver': { 'babel-module': {} }
    },
    'plugins': [
        'react',
        'babel',
        'import'
    ],
    'rules': {
        'indent': [
            'warn',
            4
        ],
        'linebreak-style': [
            'error',
            'unix'
        ],
        'quotes': [
            'warn',
            'single'
        ],
        'semi': [
            'error',
            'always'
        ],
        'no-unused-vars': [
            'warn'
        ],
    }
};
