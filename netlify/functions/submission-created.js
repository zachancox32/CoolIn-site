/**
 * Netlify fires this automatically after a form submission is stored.
 * It sends two emails through Resend:
 *   1. a confirmation to the person who filled the form in
 *   2. the lead to whoever is picking enquiries up
 *
 * Config, all set in Netlify under Site configuration > Environment variables:
 *   RESEND_API_KEY   required, from resend.com
 *   MAIL_FROM        the sender, as "Name <address>", on a verified Resend domain
 *   LEAD_TO          where the lead lands, comma separated for more than one
 *
 * No address is hardcoded here on purpose. Netlify scans the repo for the
 * values of its own environment variables and fails the build if it finds
 * them, which is the correct behaviour, so the values live only in Netlify.
 *
 * If the key is missing this does nothing and returns 200, so a
 * misconfiguration can never stop a form submission being saved.
 */

const PHONE = '07391 523255';
const SITE = 'https://cool-in.co.uk';
const NAVY = '#0D2B38';
const BLUE = '#0E6E96';
const ICE = '#5EC3E0';
const GREY = '#3D5D6E';

/** Signature block. The mark is a PNG because Gmail and Outlook strip SVG;
 *  the wordmark is real text so it still reads when images are blocked. */
const SIGNATURE = `
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:36px 0 0">
    <tr>
      <td width="64" height="3" style="background:${BLUE};font-size:0;line-height:0">&nbsp;</td>
      <td height="3" style="background:#E1EAEF;font-size:0;line-height:0">&nbsp;</td>
    </tr>
  </table>
  <p style="margin:22px 0 0">
    <img src="${SITE}/assets/img/logo-email.png" width="190" height="69"
         alt="CoolIn Cooling and Heating"
         style="display:block;border:0;width:190px;height:69px">
  </p>
  <p style="margin:16px 0 0;color:${GREY};font-size:13px;line-height:1.7">
    Lloyds House, 18-22 Lloyd Street, Manchester M2 5WA<br>
    <a href="${SITE}" style="color:${BLUE};text-decoration:none">cool-in.co.uk</a>
    <span style="color:#C7D5DD">&nbsp;&nbsp;|&nbsp;&nbsp;</span>
    <a href="tel:+447391523255" style="color:${BLUE};text-decoration:none">${PHONE}</a>
  </p>`;

const esc = (v) =>
  String(v == null ? '' : v)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

const LABELS = {
  name: 'Name', phone: 'Phone', email: 'Email', postcode: 'Postcode',
  type: 'Property', rooms: 'Rooms', message: 'Message',
};

function leadEmail(d, meta) {
  const rows = Object.keys(LABELS)
    .filter((k) => String(d[k] || '').trim())
    .map(
      (k) =>
        `<tr><td style="padding:6px 14px 6px 0;color:#667;white-space:nowrap;vertical-align:top">${LABELS[k]}</td>` +
        `<td style="padding:6px 0;color:#111"><strong>${esc(d[k])}</strong></td></tr>`
    )
    .join('');
  return `<div style="font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;font-size:15px;line-height:1.55;color:#111">
  <p style="margin:0 0 4px;font-size:18px"><strong>New enquiry from the website</strong></p>
  <p style="margin:0 0 18px;color:#667">${esc(meta)}</p>
  <table style="border-collapse:collapse">${rows}</table>
  <p style="margin:22px 0 0"><a href="tel:${esc(String(d.phone || '').replace(/\s+/g, ''))}"
     style="background:${BLUE};color:#fff;text-decoration:none;padding:11px 20px;border-radius:6px;display:inline-block">Call ${esc(d.name || 'them')} back</a></p>
</div>`;
}

function confirmEmail(d) {
  const first = String(d.name || '').trim().split(/\s+/)[0] || 'there';
  return `<div style="font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;font-size:15px;line-height:1.6;color:#111;max-width:560px">
  <p style="margin:0 0 16px">Hi ${esc(first)},</p>
  <p style="margin:0 0 16px">Thanks for getting in touch. We have your enquiry and an engineer will call you back the same working day.</p>
  <p style="margin:0 0 8px"><strong>What happens next</strong></p>
  <ol style="margin:0 0 18px;padding-left:20px">
    <li style="margin-bottom:6px">We ring you to understand the rooms and book a survey at a time that suits you.</li>
    <li style="margin-bottom:6px">Free survey at the property, usually under an hour. Measurements, wall construction, pipe routes and where the outdoor unit can legally go.</li>
    <li>A written quote, itemised and fixed, valid for 60 days. No sales visit.</li>
  </ol>
  <p style="margin:0 0 16px">If it is urgent, ring <a href="tel:+447391523255" style="color:${BLUE}">${PHONE}</a> and you will get someone rather than a machine.</p>
  ${SIGNATURE}
</div>`;
}

async function send(key, mail) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(mail),
  });
  if (!r.ok) throw new Error(`resend ${r.status}: ${await r.text()}`);
  return r.json();
}

exports.handler = async (event) => {
  const key = process.env.RESEND_API_KEY;
  if (!key) {
    console.log('RESEND_API_KEY not set, no email sent');
    return { statusCode: 200, body: 'no key' };
  }

  let payload;
  try {
    payload = JSON.parse(event.body || '{}').payload || {};
  } catch (e) {
    console.error('could not parse submission', e);
    return { statusCode: 200, body: 'bad payload' };
  }

  const d = payload.data || {};
  const from = process.env.MAIL_FROM;
  if (!from) {
    console.log('MAIL_FROM not set, no email sent');
    return { statusCode: 200, body: 'no sender' };
  }
  const leadTo = (process.env.LEAD_TO || '').split(',').map((s) => s.trim()).filter(Boolean);
  const meta = [payload.form_name || 'quote', payload.created_at || new Date().toISOString()].join(' · ');
  const where = String(d.postcode || '').trim();

  const jobs = [];

  if (leadTo.length) {
    jobs.push(
      send(key, {
        from,
        to: leadTo,
        reply_to: String(d.email || '').trim() || undefined,
        subject: `New enquiry${where ? ` from ${where}` : ''}${d.name ? `: ${d.name}` : ''}`,
        html: leadEmail(d, meta),
      })
    );
  } else {
    console.log('LEAD_TO not set, internal notification skipped');
  }

  const customer = String(d.email || '').trim();
  if (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(customer) && !d['bot-field']) {
    jobs.push(
      send(key, {
        from,
        to: [customer],
        subject: 'We have your air conditioning enquiry',
        html: confirmEmail(d),
      })
    );
  }

  const results = await Promise.allSettled(jobs);
  results.forEach((r) => r.status === 'rejected' && console.error('send failed:', r.reason));

  // Always 200. A bounced email must never look like a failed enquiry.
  return { statusCode: 200, body: JSON.stringify({ sent: results.filter((r) => r.status === 'fulfilled').length }) };
};
