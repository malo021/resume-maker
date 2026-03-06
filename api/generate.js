export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { userData } = req.body;

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: 'gpt-4o',
        max_tokens: 2000,
        messages: [{
          role: 'user',
          content: `You are a professional resume writer. Based on the following information, rewrite each section in polished, professional language suitable for a resume. Return ONLY a JSON object with these exact keys: name, email, phone, location, summary, education, experience, skills, projects. Keep the same structure but improve the language. Do not add any explanation or markdown.

User data:
${JSON.stringify(userData, null, 2)}`
        }]
      })
    });

    const data = await response.json();
    const result = data.choices[0].message.content.replace(/```json|```/g, '').trim();
    return res.status(200).json({ result: JSON.parse(result) });

  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
