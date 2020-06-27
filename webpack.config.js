const webpack = require('webpack');
const resolve = require('path').resolve;
const extname = require('path').extname;
const getFilesFromDir = require('./webpack.util.js').getFilesFromDir;
const getAliases = require('./webpack.util.js').getAliases;

const SUSOD_DIR = resolve('SUSOD');
const JS_DIR = resolve(SUSOD_DIR,'js');
const PAGE_MAINS_DIRNAME = '_routes';
const JS_PAGEMAINS_DIR = resolve(JS_DIR, PAGE_MAINS_DIRNAME);
const STATIC_DIR = resolve(SUSOD_DIR, 'static');
const JS_EXTENSIONS = ['.js', '.jsx']


const JS_MAINS = getFilesFromDir(JS_PAGEMAINS_DIR, JS_EXTENSIONS);
const entry = JS_MAINS.reduce( (obj, filePath) => {
	const entryChunkName = filePath.replace(extname(filePath), '').replace(JS_PAGEMAINS_DIR, '');
	obj[entryChunkName] = resolve('./', filePath);
	return obj;
}, {});
const aliases = getAliases(JS_MAINS, JS_DIR);

const config = {
	entry: entry,
	output:{
		path: resolve('SUSOD/static/js'),
		filename: '[name].js'
	},
	resolve: {
		extensions: JS_EXTENSIONS.concat(['.css']),
		alias: aliases
	},
	module : {
		rules: [
		{
			test: /\.(js|jsx)$/,
			loader: 'babel-loader',
			exclude: /node_modules/,
		}, {
       test: /\.(css)$/i, 
  loader:  "css-loader" 

      }
		]
	},
	
	optimization: {
		splitChunks: {
			cacheGroups: {
				vendor: {
					test: /[\\/]node_modules[\\/]/,
					chunks: 'initial',
					name: 'vendor',
					enforce: true
				}
			}
		}
	}
};

module.exports = config;