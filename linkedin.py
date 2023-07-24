const express = require('express');
const axios = require('axios');
const querystring = require('querystring');

const app = express();

const redirect_uri = 'http://localhost:3000/auth/linkedin/callback';  // should match with the redirect URL in LinkedIn Developer Portal
const client_id = 'YOUR_LINKEDIN_CLIENT_ID';
const client_secret = 'YOUR_LINKEDIN_CLIENT_SECRET';

app.get('/auth/linkedin', (req, res) => {
  const scope = 'r_liteprofile r_emailaddress';
  res.redirect(`https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${client_id}&redirect_uri=${redirect_uri}&state=foobar&scope=${scope}`);
});

app.get('/auth/linkedin/callback', async (req, res) => {
  const { code } = req.query;
  try {
    const { data } = await axios({
      url: 'https://www.linkedin.com/oauth/v2/accessToken',
      method: 'post',
      data: querystring.stringify({
        grant_type: 'authorization_code',
        code,
        redirect_uri,
        client_id,
        client_secret,
      }),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    const accessToken = data.access_token;
    const profile = await axios({
      url: 'https://api.linkedin.com/v2/me',
      method: 'get',
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    res.send(profile.data);
  } catch (error) {
    res.send(error);
  }
});

app.listen(3000, () => console.log('Listening on port 3000'));
