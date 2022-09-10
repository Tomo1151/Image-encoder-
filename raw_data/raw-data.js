const PNG = require('pngjs').PNG;
const fs = require('fs');

if (process.argv[2] == null) {
  console.log("Usage: `node raw-data.js \u001b[31m[file_name]`\u001b[0m")
  return -1;
}

fs.createReadStream(process.argv[2])
.pipe(
  new PNG({
  	deflateLevel: 9,
  	colorType: 2
  })
)
.on("parsed", function () {
  this.pack().pipe(fs.createWriteStream("LZ/temp/.cache"));
});