const crypto = require("crypto");

const DEFAULT_TOKEN = "pAHDfJIqYTu8ri4Yz3T6Zx64vQaXNn4YFA8e4O6z8fKpgNNV";

module.exports = (req, res) => {
  const token = process.env.EBAY_VERIFICATION_TOKEN || DEFAULT_TOKEN;
  const host = req.headers["x-forwarded-host"] || req.headers.host || "";
  if (req.method === "GET") {
    const u = new URL(req.url, "https://" + host);
    const challenge = u.searchParams.get("challenge_code") || "";
    const endpoint = "https://" + host + u.pathname;
    const hash = crypto
      .createHash("sha256")
      .update(challenge + token + endpoint)
      .digest("hex");
    res.setHeader("Content-Type", "application/json");
    res.status(200).send(JSON.stringify({ challengeResponse: hash }));
  } else {
    res.status(200).end();
  }
};

