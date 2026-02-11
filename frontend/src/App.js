import React, {useState} from 'react';
import axios from 'axios';

function App(){
  const [commentsText, setCommentsText] = useState('');
  const [subject, setSubject] = useState('AI');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    const comments = commentsText.split('\n').map(s => s.trim()).filter(Boolean);
    setLoading(true);
    try{
      // Use explicit backend URL so the frontend works without a dev proxy
      const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const resp = await axios.post(`${API_BASE}/api/analyze/`, {subject, comments});
      setResult(resp.data);
    }catch(e){
      alert('Request failed: ' + (e.response?.data?.error || e.message));
    }finally{setLoading(false)}
  }

  return (
    <div style={{maxWidth:800, margin:'24px auto', fontFamily: 'Inter, Roboto, Arial'}}>
      <h1>Student Feedback - Analyzer</h1>
      <label>Subject</label>
      <select value={subject} onChange={e=>setSubject(e.target.value)}>
        <option>Artificial Intelligence</option>
        <option> Optimization Techniques</option>
      </select>
      <label style={{display:'block', marginTop:12}}>Paste comments (one per line)</label>
      <textarea style={{width:'100%', height:180}} value={commentsText} onChange={e=>setCommentsText(e.target.value)} />
      <div style={{marginTop:12}}>
        <button onClick={submit} disabled={loading}>Analyze</button>
      </div>

      {result && (
        <div style={{marginTop:20}}>
          <h2>Summary</h2>
          <pre>{JSON.stringify(result.summary, null, 2)}</pre>
          <h3>Interpretations</h3>
          <ul>{result.interpretations.map((r,i)=><li key={i}>{r}</li>)}</ul>
          <h3>Wordcloud</h3>
          <img src={result.wordcloud_url} style={{maxWidth:'100%'}} alt="wordcloud" />
        </div>
      )}
    </div>
  )
}

export default App;
