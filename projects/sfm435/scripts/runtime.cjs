// Motion Canvas settings are task-local, without writing to the account home.
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve('.runtime');
fs.mkdirSync(root,{recursive:true});
require('node:os').homedir=()=>root;
