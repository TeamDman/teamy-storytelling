const path=require('node:path');const fs=require('node:fs');
const directory=path.join(__dirname,'.settings');fs.mkdirSync(directory,{recursive:true});
require('node:os').homedir=()=>directory;
