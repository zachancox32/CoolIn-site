/**
 * Netlify runs this automatically when a deploy has gone live. It tells Bing
 * and the other IndexNow engines (Yandex, Seznam, Naver) which pages exist,
 * by posting every address in the live sitemap.
 *
 * It runs after the deploy, not during the build, so the engines are only
 * told about pages, and the key file, once they can actually be fetched. A
 * submission made during the build named pages that did not exist yet.
 *
 * The key is public by design: it is also served at /<key>.txt, which is how
 * the engines check the submission came from the site. tools/indexnow.py
 * fails the build if this copy and tools/indexnow-key.txt ever disagree.
 *
 * Never throws: a search engine being unreachable must not mark anything as
 * failed. Only production deploys submit.
 */

const KEY = '8c997d24cb381ed6d9323670a6827cee';
const SITE = 'https://cool-in.co.uk';
const ENDPOINT = 'https://api.indexnow.org/indexnow';

exports.handler = async (event) => {
  try {
    const { payload = {} } = JSON.parse(event.body || '{}');
    if (payload.context && payload.context !== 'production') {
      console.log('indexnow: skipped on', payload.context);
      return { statusCode: 200, body: 'skipped' };
    }
    const xml = await (await fetch(`${SITE}/sitemap.xml`)).text();
    const urlList = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]).slice(0, 10000);
    if (!urlList.length) {
      console.log('indexnow: live sitemap had no urls');
      return { statusCode: 200, body: 'empty' };
    }
    const r = await fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ host: new URL(SITE).host, key: KEY, keyLocation: `${SITE}/${KEY}.txt`, urlList }),
    });
    console.log('indexnow: submitted', urlList.length, 'urls,', r.status, (await r.text()).slice(0, 200));
  } catch (e) {
    console.log('indexnow: failed,', e && e.message);
  }
  return { statusCode: 200, body: 'ok' };
};
