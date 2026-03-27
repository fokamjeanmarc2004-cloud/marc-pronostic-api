const https = require('https');

const CLAUDE_KEY = 'sk-ant-api03-EXA0AuT9AoGwktgcU02e3GRQWZFNUr9SGwpPUMZfSd3AruL0NjIOcawf0wUFIR73U5kWUE7_Vl_EfWBQpq_k0Q-qctvSQAA';
const PORT = process.env.PORT || 3000;

function sendJSON(res, status, data) {
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  });
  res.end(JSON.stringify(data));
}

require('http').createServer(function(req, res) {

  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(200, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    });
    return res.end();
  }

  // Health check
  if (req.method === 'GET' && req.url === '/') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    return res.end('Marc Pronostic API - OK');
  }

  // Analyze endpoint
  if (req.method === 'POST' && req.url === '/analyze') {
    var body = '';
    req.on('data', function(chunk) { body += chunk.toString(); });
    req.on('end', function() {
      try {
        var data = JSON.parse(body);
        var home = data.home || '';
        var away = data.away || '';
        var comp = data.competition || 'Football';
        var type = data.type || 'all';
        var ctx  = data.context || '';

        var prompt = 'Tu es un expert en pronostics sportifs professionnels. Analyse ce match avec precision.\n\n'
          + 'Match : ' + home + ' vs ' + away + '\n'
          + 'Competition : ' + comp + '\n'
          + (ctx ? 'Contexte : ' + ctx + '\n' : '')
          + '\nDonne une analyse complete avec ces 5 predictions :\n'
          + '1. Pair ou Impair (total de buts)\n'
          + '2. Over ou Under 2.5 buts\n'
          + '3. BTTS - Les deux equipes marquent (Oui ou Non)\n'
          + '4. Resultat 1X2 (1=domicile gagne, X=nul, 2=exterieur gagne)\n'
          + '5. Over ou Under 1.5 buts\n\n'
          + 'Reponds UNIQUEMENT en JSON pur sans markdown :\n'
          + '{'
          + '"pairPct":54,"impairPct":46,'
          + '"over25Pct":60,"under25Pct":40,'
          + '"bttsPct":55,"noBttsPct":45,'
          + '"res1Pct":45,"resXPct":28,"res2Pct":27,'
          + '"over15Pct":75,"under15Pct":25,'
          + '"mainPrediction":"PAIR",'
          + '"confidence":68,'
          + '"analysis":"Analyse detaillee 4-5 phrases en francais expliquant la forme des equipes, les stats de buts, et pourquoi ces predictions.",'
          + '"keyFactors":["facteur 1","facteur 2","facteur 3"]'
          + '}';

        var postData = JSON.stringify({
          model: 'claude-haiku-4-5-20251001',
          max_tokens: 1000,
          messages: [{ role: 'user', content: prompt }]
        });

        var options = {
          hostname: 'api.anthropic.com',
          port: 443,
          path: '/v1/messages',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': CLAUDE_KEY,
            'anthropic-version': '2023-06-01',
            'Content-Length': Buffer.byteLength(postData)
          }
        };

        var apiReq = https.request(options, function(apiRes) {
          var result = '';
          apiRes.on('data', function(chunk) { result += chunk; });
          apiRes.on('end', function() {
            try {
              var parsed = JSON.parse(result);
              var text   = parsed.content && parsed.content[0] ? parsed.content[0].text : '';
              var clean  = text.replace(/```json/g,'').replace(/```/g,'').trim();
              var m      = clean.match(/\{[\s\S]*\}/);
              if (!m) throw new Error('no json');
              var analysis = JSON.parse(m[0]);
              sendJSON(res, 200, { success: true, data: analysis });
            } catch(e) {
              sendJSON(res, 500, { success: false, error: 'Parse error: ' + e.message });
            }
          });
        });

        apiReq.on('error', function(e) {
          sendJSON(res, 500, { success: false, error: e.message });
        });

        apiReq.write(postData);
        apiReq.end();

      } catch(e) {
        sendJSON(res, 400, { success: false, error: 'Invalid request: ' + e.message });
      }
    });
    return;
  }

  sendJSON(res, 404, { error: 'Not found' });

}).listen(PORT, function() {
  console.log('Marc Pronostic API running on port ' + PORT);
});
