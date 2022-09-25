const PNG = require('pngjs').PNG;
const fs = require('fs');

if (!fs.existsSync('LZ/temp/sheared.data')) {
  console.log("sheared.data does not exist.")
  return 1;
}

fs.createReadStream('LZ/temp/sheared.data')
.pipe(
  new PNG({
  	deflateLevel: 9,
  	colorType: 2
  })
)
.on("parsed", function () {
  this.pack().pipe(fs.createWriteStream("LZ/temp/.cache"));
});