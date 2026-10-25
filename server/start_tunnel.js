const http = require('http');
const { exec } = require('child_process');
const localtunnel = require('localtunnel');

function checkPort(port) {
  return new Promise((resolve) => {
    const req = http.get(`http://127.0.0.1:${port}/api/v1/listings`, (res) => {
      resolve(true);
    });
    req.on('error', () => resolve(false));
    req.setTimeout(1500, () => {
      req.destroy();
      resolve(false);
    });
  });
}

(async () => {
  console.log('===================================================================');
  console.log('  KHOI DONG HE THONG WEBSITE ONLINE (BACKEND + DATABASE + TUNNEL)  ');
  console.log('===================================================================\n');

  // 1. Kiem tra xem Server port 5000 da chay chua, neu chua thi tu khoi dong
  const isRunning = await checkPort(5000);
  if (!isRunning) {
    console.log('[1/3] May chu port 5000 chua chay. Dang tu dong khoi dong Server & Database...');
    require('./server.js');
    // Doi 1.5 giay cho Express khoi tao xong
    await new Promise(r => setTimeout(r, 1500));
  } else {
    console.log('[1/3] May chu port 5000 da san sang hoat dong.');
  }

  // 2. Lay IP cong khai lam mat khau loca.lt neu trang yeu cau
  let publicIp = '';
  try {
    const ipRes = await fetch('https://api.ipify.org');
    publicIp = (await ipRes.text()).trim();
  } catch (e) {
    publicIp = 'Lay tu https://loca.lt/mytunnelpassword';
  }
  console.log('[2/3] IP mang cong khai cua ban (Tunnel Password): ' + publicIp);

  // 3. Ket noi Localtunnel
  console.log('[3/3] Dang cap duong link HTTPS cong khai...');
  try {
    const tunnel = await localtunnel({ port: 5000 });

    console.log('\n===================================================================');
    console.log('           CHUC MUNG! WEBSITE DA ONLINE THANH CONG!                ');
    console.log('===================================================================');
    console.log('>> DUONG LINK TRUY CAP: ' + tunnel.url);
    console.log('>> MAT KHAU XAC MINH (neu web hien bang hoi): ' + publicIp);
    console.log('===================================================================');
    console.log('Huong dan truy cap:');
    console.log('1. Nhap hoac click vao duong link tren de vao web.');
    console.log('2. Neu trang hien "Friendly Reminder: Submit your Endpoint IP",');
    console.log('   ban chi can paste so IP ' + publicIp + ' vao o roi bam Submit.');
    console.log('3. Giu nguyen cua so nay de website luon hoat dong truc tuyen.\n');

    tunnel.on('close', () => {
      console.log('Tunnel da dong.');
    });
  } catch (err) {
    console.error('Loi tao tunnel:', err);
  }
})();
