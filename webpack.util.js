const readdirSync = require('fs').readdirSync;
const statSync = require('fs').statSync;
const join = require('path').join;
const extname = require('path').extname;
const fileParse = require('path').parse;
const dirname = require('path').dirname;
const basename = require('path').basename;
const sep = require('path').sep;

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

// returns directory to entry point's folder for alias
// const getPageGroups = (entryPoints) => {
// 	entryPoints.reduce( (obj, entry) => {
// 		const curFile = fileParse(entry).base;
// 		const curFileName = curFile.replace(extname(curFile), '');
// 		obj[curFileName] = dirname(entry).replace(basename(dirname(entry)), '');
// 	}, {})
// }

module.exports = getFilesFromDir;
//module.exports = getPageGroups;