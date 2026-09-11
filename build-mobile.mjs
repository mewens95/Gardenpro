import { existsSync, mkdirSync, rmSync, copyFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { platform } from 'node:os';

const root = process.cwd();
const webDir = `${root}/www`;

rmSync(webDir, { recursive: true, force: true });
mkdirSync(webDir, { recursive: true });

for (const file of ['index.html', 'manifest.webmanifest', 'sw.js', 'icon-192.png', 'icon-512.png']) {
  copyFileSync(`${root}/${file}`, `${webDir}/${file}`);
}

const npx = platform() === 'win32' ? 'npx.cmd' : 'npx';
if (!existsSync(`${root}/android`)) {
  execFileSync(npx, ['cap', 'add', 'android'], { stdio: 'inherit', cwd: root });
}
execFileSync(npx, ['cap', 'sync', 'android'], { stdio: 'inherit', cwd: root });

const gradle = platform() === 'win32' ? 'gradlew.bat' : './gradlew';
execFileSync(gradle, ['bundleRelease'], { stdio: 'inherit', cwd: `${root}/android` });

console.log('Release AAB created at android/app/build/outputs/bundle/release/app-release.aab');
