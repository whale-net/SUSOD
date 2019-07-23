const webpack = require('webpack');
const resolve = require('path').resolve;
const config = {
	entry: __dirname + '/SUSOD/js/main.jsx',
	output:{
		path: resolve('SUSOD/static/js'),
		filename: 'bundle.js',
	},
	resolve: {
		extensions: ['.js','.jsx','.css']
	},
	module : {
		rules: [
		{
			test: /\.(js|jsx)$/,
			loader: 'babel-loader',
			exclude: /node_modules/,
		}
		]
	},
};

module.exports = config;