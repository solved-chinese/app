module.exports = {
    'env': {
        'browser': true,
        'es2021': true,
        'amd': true
    },
    'globals': {
        'JSX': true,
        'window': true,
        'module': true
    },
    'extends': [
        'eslint:recommended',
        'plugin:react/recommended',
        'plugin:@typescript-eslint/eslint-recommended',
        'plugin:@typescript-eslint/recommended'
    ],
    'parser': '@typescript-eslint/parser',
    'parserOptions': {
        'ecmaFeatures': {
            'jsx': true
        },
        'ecmaVersion': 12,
        'sourceType': 'module'
    },
    'settings': {
        'import/resolver': { 
            'babel-module': {}
        },
        'react': {
            'pragma': 'React',
            'version': 'detect',
        }
    },
    'plugins': [
        'react',
        'babel',
        'import',
        '@typescript-eslint'
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
        '@typescript-eslint/no-non-null-assertion': 0
    }
};
