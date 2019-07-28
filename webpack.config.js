const webpack = require('webpack');
const resolve = require('path').resolve;
const extname = require('path').extname;
const getFilesFromDir = require('./webpack.util.js');
//const getPageGroups = require('./webpack.util.js');

const SUSOD_DIR = resolve('SUSOD');
const JS_DIR = resolve(SUSOD_DIR,'js');
const PAGE_GROUP_DIRNAME = 'page_groups';
const JS_PAGEGROUPS_DIR = resolve(JS_DIR, PAGE_GROUP_DIRNAME);
const STATIC_DIR = resolve(SUSOD_DIR, 'static');
const JS_EXTENSIONS = ['.js', '.jsx']



const entry = getFilesFromDir(JS_PAGEGROUPS_DIR, JS_EXTENSIONS).reduce( (obj, filePath) => {
	const entryChunkName = filePath.replace(extname(filePath), '').replace(JS_PAGEGROUPS_DIR, '');
	obj[entryChunkName] = resolve('./', filePath);
	return obj;
}, {});
console.log(getFilesFromDir(JS_PAGEGROUPS_DIR, JS_EXTENSIONS));
console.log(entry);
console.log(resolve(JS_PAGEGROUPS_DIR, 'index.jsx'));
//console.log(getPageGroups(entry));

const config = {
	entry: entry,
	output:{
		path: resolve('SUSOD/static/js'),
		filename: 'bundle.js',
	},
	resolve: {
		extensions: JS_EXTENSIONS.concat(['.css']),
		alias: {
			index: resolve(JS_PAGEGROUPS_DIR, 'index.jsx')
		}
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