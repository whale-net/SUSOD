const readdirSync = require('fs').readdirSync;
const statSync = require('fs').statSync;
const join = require('path').join;
const extname = require('path').extname;
const fileParse = require('path').parse;
const resolve = require('path').resolve;

//https://github.com/przemek-nowicki/multi-page-app-with-react/blob/master/config/files.js
const getFilesFromDir = (dir, fileTypes) => {
	const filesToReturn = [];
	const walkDir = (currentPath) => {
		const files = readdirSync(currentPath);
		for (let i in files) {
			const curFile = join(currentPath, files[i]);
			if (statSync(curFile).isFile() && fileTypes.indexOf(extname(curFile)) != -1) {
				filesToReturn.push(curFile);
			} else if (statSync(curFile).isDirectory()) {
				walkDir(curFile);
			}
		}
	}
	walkDir(dir);
	return filesToReturn;
}

//returns directory to entry point's folder for alias
const getAliases = (entryPoints, JS_DIR) => {
	aliases = {}
	entryPoints.forEach( (entry) => {
		const curFile = fileParse(entry).base;
		const curFileName = curFile.replace(extname(curFile), '');
		aliases[curFileName] = resolve(JS_DIR, curFileName);
	})
	return aliases;
}

module.exports ={
	getFilesFromDir: getFilesFromDir,	
	getAliases: getAliases
} 
