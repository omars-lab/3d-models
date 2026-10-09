---
date: 2026-10-02
---

# The printer's certificate is pinned, and a small relay carries the camera stream

*Issue slug: `camera-tls-pin`. Written 2026-10-02, while making `bambu status camera` work so a
send can show the bed first ("can we also pull screenshot from bambu camera to confirm its
empty", Omar).*

## What was tried first, and why it broke

The camera on X1/H2-class printers is RTSP over TLS on port 322
(`rtsps://bblp:<access code>@<host>:322/streaming/live/1`), and ffmpeg can take one frame from it.
The first version handed that URL to ffmpeg. ffmpeg 8 checks the printer's certificate, and the
check failed: `certificate verify failed`.

What the printer sends: one certificate naming its serial (`CN=<the printer serial>`), issued by
"BBL Device CA N6-V2", valid 2026-04-16 to 2036. It does not send the CA certificate. So the check
needs that CA from somewhere else, and nowhere here has it:

- Bambu Studio ships `Contents/Resources/cert/printer.cer` with three Bambu CAs (BBL CA, BBL CA2
  RSA, BBL CA2 ECC), but not N6-V2. Checking against it fails with "unable to get local issuer
  certificate".
- Turning ffmpeg's check off (`-tls_verify 0`) was refused by the session's safety check as a
  weakening of TLS. That refusal was right. The access code rides in the camera URL, so an
  unchecked connection hands it to anything on the LAN that answers on 322.
- ffmpeg cannot trust a single certificate on its own:
  `-ca_file <the printer's cert> -verifyhost <serial>` still fails, because OpenSSL wants a
  chain that ends at a CA.

## What replaced it

Omar picked pinning (2026-10-02): save this printer's own certificate once, then accept exactly
that certificate and no other.

1. **`bambu setup printer-pin`** (first called `camera-pin`, which still works) fetches the
   certificate with `openssl s_client` (this sends no credentials). Since 2026-10-04 it fetches
   from port 8883, which answers whenever LAN mode is on; 322 also needs Liveview. It checks that the certificate names the configured serial and is in date, then
   saves it to `.bambu/printer-<serial>.pem`, which is gitignored and local to this machine. It
   prints the issuer, the expiry and the SHA-256 fingerprint.
2. **Node does the TLS hop, pinned.** Node can trust a single certificate:
   `ca: <pinned cert>` with `allowPartialTrustChain: true` lets the pinned certificate stand in
   for the CA. OpenSSL still checks the signature, the dates and the key. On top of that, the name
   must equal the serial and the fingerprint must match the pin. The tests make a stand-in printer
   with the same shape (a leaf naming the serial, its CA never sent). They show that the pinned
   certificate connects, that a different certificate naming the same serial is refused, and that
   a certificate naming another serial is refused (`tools/bambu/src/backends/tls-pin.test.ts`).
3. **A relay on 127.0.0.1 carries ffmpeg's plain RTSP to the pinned TLS connection.** Two things
   the printer does shaped it:
   - It answers any URL that is not its own `rtsps://<host>:322/…` with
     `301 Redirecting to rtsps://<host>/1`, so ffmpeg followed the redirect straight into the
     unpinned check. The relay rewrites URLs in the RTSP text messages both ways and leaves the
     video frames (`$`-framed) untouched byte for byte.
   - It uses Digest auth (LIVE555, `realm="LIVE555 Streaming Media"`, no qop), and Digest signs
     the URL, so ffmpeg's signature over its loopback URL fails after the rewrite (`401`).
     The relay signs each request again with the real access code. ffmpeg gets a placeholder
     password (`relay`), so **the access code is no longer in ffmpeg's arguments** (which any
     process can read with `ps`) and never crosses loopback. The code only travels inside the
     pinned TLS connection.

First frame 2026-10-02: 1920×1080 JPEG, ~300 KB, the empty textured plate.
`bambu print send` now saves one frame under `.bambu/bed/` before the confirm and on `--dry-run`,
and says where it is (`--no-bed-photo` skips it). A failed photo warns and does not block: the
person sending can still look at the bed. Spotting objects is the X2D's own job once it starts
(D-092); the photo is for the person.

## What it commits us to

- **Re-pin after a factory reset or a new certificate.** Every connection then refuses with a
  message that says to run `bambu setup printer-pin` again. The current certificate expires 2036-04-13.
- **The first fetch is trusted as it comes.** The pin is only as good as the network was the
  moment it was taken. That is the usual price of pinning.
- **No connection without a pin.** `status`, `storage`, `print send` and the camera all refuse
  until `bambu setup printer-pin` has run once; `bambu setup doctor` marks a missing pin `✗`.

## MQTT and FTPS check the same pin (2026-10-04)

Until then MQTT (8883) and FTPS (990) skipped the certificate check (`rejectUnauthorized: false`),
and both carry the access code: MQTT as its password, FTPS as its login. Fetching what each port
presents showed the same certificate as the camera's: the same SHA-256 fingerprint
(`7A:61:0F:AE:…:EB:A8:5D:FF`), `CN=<the printer serial>`, valid to 2036-04-13. The one difference is
that 8883 and 990 also send the intermediate "BBL Device CA N6-V2" (issued by "BBL CA2 RSA"),
where 322 sends the certificate alone. The pinned options do not depend on that: the pinned
certificate is the trust anchor whatever the server sends after it.

So the helpers moved to `tools/bambu/src/backends/tls-pin.ts`, and MQTT and FTPS use them.
`mqtt` and `basic-ftp` both hand their TLS options to Node unchanged, and `basic-ftp` reuses them on
every data connection, so a file listing or an upload is pinned too. The tests serve both shapes
(certificate alone, certificate with its CA), and run the pinned options through `mqtt.connect` and
`basic-ftp`'s implicit-TLS connect: the printer's certificate connects, and one naming the same
serial under another CA is refused before any password is sent. Checked against the X2D the same
day: `bambu status show`, `bambu storage list` and `bambu status camera` all connected with the pin.
