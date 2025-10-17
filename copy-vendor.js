// scripts/copy-vendor.js
const fs = require("fs");
const path = require("path");

// Find project root by looking for manage.py
function findProjectRoot(startDir) {
  let current = startDir;
  while (current !== path.parse(current).root) {
    if (fs.existsSync(path.join(current, "manage.py"))) {
      return current;
    }
    current = path.dirname(current);
  }
  throw new Error("Could not find manage.py — run this from inside a Django project");
}

const projectRoot = findProjectRoot(__dirname);
const vendor = path.join(projectRoot, "static", "vendor");

function copyFile(src, dest) {
  const dir = path.dirname(dest);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`Created folder: ${dir}`);
  }
  fs.copyFileSync(src, dest);
  console.log(`Copied: ${src} -> ${dest}`);
}

// ✅ Libraries to copy
copyFile("node_modules/bootstrap/dist/css/bootstrap.min.css", path.join(vendor, "bootstrap/css/bootstrap.min.css"));
copyFile("node_modules/bootstrap/dist/js/bootstrap.bundle.min.js", path.join(vendor, "bootstrap/js/bootstrap.bundle.min.js"));

copyFile("node_modules/bootstrap-icons/font/bootstrap-icons.css", path.join(vendor, "bootstrap-icons/bootstrap-icons.css"));
fs.cpSync("node_modules/bootstrap-icons/font/fonts", path.join(vendor, "bootstrap-icons/fonts"), { recursive: true });

copyFile("node_modules/jquery/dist/jquery.min.js", path.join(vendor, "jquery/jquery.min.js"));

copyFile("node_modules/apexcharts/dist/apexcharts.min.js", path.join(vendor, "apexcharts/apexcharts.min.js"));

copyFile("node_modules/datatables.net-bs5/css/dataTables.bootstrap5.min.css", path.join(vendor, "datatables/css/datatables.min.css"));
copyFile("node_modules/datatables.net-bs5/js/dataTables.bootstrap5.min.js", path.join(vendor, "datatables/js/datatables.min.js"));

console.log("\n✅ All vendor libraries copied to:", vendor);
