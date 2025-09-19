import React, { useState, useEffect } from 'react';

const teams = [
  { id: 1, name: 'Đội 1', players: ['Quân', 'Quỳnh'], group: 'A' },
  { id: 2, name: 'Đội 2', players: ['Thông', 'Linh'], group: 'A' },
  { id: 3, name: 'Đội 3', players: ['Thành', 'Sơn'], group: 'A' },
  { id: 4, name: 'Đội 4', players: ['Minh', 'Quang'], group: 'A' },
  { id: 5, name: 'Đội 5', players: ['Tú', 'Tiến'], group: 'B' },
  { id: 6, name: 'Đội 6', players: ['Tuấn', 'Diệp'], group: 'B' },
  { id: 7, name: 'Đội 7', players: ['Vơn', 'Ngân'], group: 'B' },
  { id: 8, name: 'Đội 8', players: ['Trung', 'Kiên'], group: 'B' },
];

const initialGroupMatches = [
  // Group A
  { id: 'A1', team1: teams[0], team2: teams[1], score1: null, score2: null, stage: 'group', group: 'A' },
  { id: 'A2', team1: teams[2], team2: teams[3], score1: null, score2: null, stage: 'group', group: 'A' },
  { id: 'A3', team1: teams[0], team2: teams[2], score1: null, score2: null, stage: 'group', group: 'A' },
  { id: 'A4', team1: teams[1], team2: teams[3], score1: null, score2: null, stage: 'group', group: 'A' },
  { id: 'A5', team1: teams[1], team2: teams[2], score1: null, score2: null, stage: 'group', group: 'A' },
  { id: 'A6', team1: teams[0], team2: teams[3], score1: null, score2: null, stage: 'group', group: 'A' },
  // Group B
  { id: 'B1', team1: teams[5], team2: teams[7], score1: null, score2: null, stage: 'group', group: 'B' },
  { id: 'B2', team1: teams[6], team2: teams[7], score1: null, score2: null, stage: 'group', group: 'B' },
  { id: 'B3', team1: teams[4], team2: teams[6], score1: null, score2: null, stage: 'group', group: 'B' },
  { id: 'B4', team1: teams[4], team2: teams[5], score1: null, score2: null, stage: 'group', group: 'B' },
  { id: 'B5', team1: teams[5], team2: teams[6], score1: null, score2: null, stage: 'group', group: 'B' },
  { id: 'B6', team1: teams[4], team2: teams[7], score1: null, score2: null, stage: 'group', group: 'B' },
];

function App() {
  const [matches, setMatches] = useState(initialGroupMatches);
  const [currentStage, setCurrentStage] = useState('group');
  const [groupStandings, setGroupStandings] = useState({ A: [], B: [] });

  useEffect(() => {
    const calculateStanding = (groupTeams, groupMatches) => {
      const standings = groupTeams.map(team => ({
        team,
        wins: 0,
        losses: 0,
        pointsFor: 0,
        pointsAgainst: 0,
        pointsDiff: 0,
      }));

      groupMatches.forEach(match => {
        if (match.score1 !== null && match.score2 !== null) {
          const team1Standing = standings.find(s => s.team.id === match.team1.id);
          const team2Standing = standings.find(s => s.team.id === match.team2.id);

          team1Standing.pointsFor += match.score1;
          team1Standing.pointsAgainst += match.score2;
          team2Standing.pointsFor += match.score2;
          team2Standing.pointsAgainst += match.score1;

          if (match.score1 > match.score2) {
            team1Standing.wins++;
            team2Standing.losses++;
          } else if (match.score2 > match.score1) {
            team2Standing.wins++;
            team1Standing.losses++;
          }
        }
      });

      standings.forEach(s => {
        s.pointsDiff = s.pointsFor - s.pointsAgainst;
      });

      standings.sort((a, b) => {
        if (b.wins !== a.wins) return b.wins - a.wins;
        if (b.pointsDiff !== a.pointsDiff) return b.pointsDiff - a.pointsDiff;
        return b.pointsFor - a.pointsFor;
      });

      return standings;
    };

    const groupAMatches = matches.filter(m => m.group === 'A');
    const groupBMatches = matches.filter(m => m.group === 'B');

    setGroupStandings({
      A: calculateStanding(teams.filter(t => t.group === 'A'), groupAMatches),
      B: calculateStanding(teams.filter(t => t.group === 'B'), groupBMatches),
    });
  }, [matches]);

  const updateScore = (matchId, teamNumber, value) => {
    const score = value === '' ? null : parseInt(value, 10);
    setMatches(prev =>
      prev.map(m =>
        m.id === matchId
          ? { ...m, [teamNumber === 1 ? 'score1' : 'score2']: score }
          : m
      )
    );
  };

  const generateKnockoutMatches = () => {
    if (groupStandings.A.length < 2 || groupStandings.B.length < 2) return;

    const semiMatches = [
      { id: 'SF1', team1: groupStandings.A[0].team, team2: groupStandings.B[1].team, score1: null, score2: null, stage: 'semi' },
      { id: 'SF2', team1: groupStandings.B[0].team, team2: groupStandings.A[1].team, score1: null, score2: null, stage: 'semi' },
    ];

    setMatches(prev => [...prev.filter(m => m.stage === 'group'), ...semiMatches]);
    setCurrentStage('semi');
  };

  const generateFinalMatches = () => {
    const semiMatches = matches.filter(m => m.stage === 'semi');
    if (semiMatches.length < 2) return;

    const sf1 = semiMatches.find(m => m.id === 'SF1');
    const sf2 = semiMatches.find(m => m.id === 'SF2');

    if (
      !sf1 || !sf2 ||
      sf1.score1 === null || sf1.score2 === null ||
      sf2.score1 === null || sf2.score2 === null
    ) return;

    const sf1Winner = sf1.score1 > sf1.score2 ? sf1.team1 : sf1.team2;
    const sf2Winner = sf2.score1 > sf2.score2 ? sf2.team1 : sf2.team2;

    const finalMatch = { id: 'FINAL', team1: sf1Winner, team2: sf2Winner, score1: null, score2: null, stage: 'final' };

    setMatches(prev => [...prev.filter(m => m.stage !== 'final'), finalMatch]);
    setCurrentStage('final');
  };

  const getRankingList = () => {
    const finalMatch = matches.find(m => m.stage === 'final');
    const semiMatches = matches.filter(m => m.stage === 'semi');

    if (!finalMatch || finalMatch.score1 === null || finalMatch.score2 === null) return [];

    const champion = finalMatch.score1 > finalMatch.score2 ? finalMatch.team1 : finalMatch.team2;
    const runnerUp = finalMatch.score1 > finalMatch.score2 ? finalMatch.team2 : finalMatch.team1;

    if (semiMatches.length < 2) return [];

    const sf1 = semiMatches.find(m => m.id === 'SF1');
    const sf2 = semiMatches.find(m => m.id === 'SF2');

    if (!sf1 || !sf2 || sf1.score1 === null || sf1.score2 === null || sf2.score1 === null || sf2.score2 === null) return [];

    const sf1Loser = sf1.score1 > sf1.score2 ? sf1.team2 : sf1.team1;
    const sf2Loser = sf2.score1 > sf2.score2 ? sf2.team2 : sf2.team1;

    return [
      { position: 1, team: champion, title: '🏆 Vô địch' },
      { position: 2, team: runnerUp, title: '🥈 Á quân' },
      { position: 3, team: sf1Loser, title: '🥉 Đồng giải 3' },
      { position: 3, team: sf2Loser, title: '🥉 Đồng giải 3' },
    ];
  };

  return (
    <div style={{ maxWidth: 600, margin: 'auto', padding: 20, fontFamily: 'Arial, sans-serif' }}>
      <header style={{ backgroundColor: '#b8860b', color: 'white', padding: 20, textAlign: 'center', borderRadius: 8 }}>
        <h1>🏓 Giải Pickleball</h1>
        <p>Hệ thống xếp hạng tự động</p>
      </header>

      <nav style={{ marginTop: 20, marginBottom: 20, textAlign: 'center' }}>
        {['group', 'semi', 'final'].map(stage => (
          <button
            key={stage}
            onClick={() => setCurrentStage(stage)}
            style={{
              margin: '0 5px',
              padding: '8px 16px',
              backgroundColor: currentStage === stage ? '#1e40af' : 'transparent',
              color: currentStage === stage ? 'white' : '#1e40af',
              border: '1px solid #1e40af',
              borderRadius: 4,
              cursor: 'pointer',
            }}
          >
            {stage === 'group' ? 'Vòng bảng' : stage === 'semi' ? 'Bán kết' : 'Chung kết'}
          </button>
        ))}
      </nav>

      {currentStage === 'group' && (
        <>
          <section>
            <h2 style={{ color: '#1e40af' }}>Bảng A - Lịch thi đấu</h2>
            {matches.filter(m => m.group === 'A').map(match => (
              <div key={match.id} style={{ border: '1px solid #ccc', borderRadius: 6, padding: 10, marginBottom: 10 }}>
                <div><strong>{match.id}</strong></div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div>{match.team1.name}</div>
                    <small>{match.team1.players.join(' + ')}</small>
                  </div>
                  <input
                    type="number"
                    min="0"
                    value={match.score1 ?? ''}
                    onChange={e => updateScore(match.id, 1, e.target.value)}
                    style={{ width: 40, textAlign: 'center' }}
                  />
                  <span> - </span>
                  <input
                    type="number"
                    min="0"
                    value={match.score2 ?? ''}
                    onChange={e => updateScore(match.id, 2, e.target.value)}
                    style={{ width: 40, textAlign: 'center' }}
                  />
                  <div>
                    <div>{match.team2.name}</div>
                    <small>{match.team2.players.join(' + ')}</small>
                  </div>
                </div>
              </div>
            ))}
          </section>

          <section>
            <h2 style={{ color: '#1e40af' }}>Bảng B - Lịch thi đấu</h2>
            {matches.filter(m => m.group === 'B').map(match => (
              <div key={match.id} style={{ border: '1px solid #ccc', borderRadius: 6, padding: 10, marginBottom: 10 }}>
                <div><strong>{match.id}</strong></div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div>{match.team1.name}</div>
                    <small>{match.team1.players.join(' + ')}</small>
                  </div>
                  <input
                    type="number"
                    min="0"
                    value={match.score1 ?? ''}
                    onChange={e => updateScore(match.id, 1, e.target.value)}
                    style={{ width: 40, textAlign: 'center' }}
                  />
                  <span> - </span>
                  <input
                    type="number"
                    min="0"
                    value={match.score2 ?? ''}
                    onChange={e => updateScore(match.id, 2, e.target.value)}
                    style={{ width: 40, textAlign: 'center' }}
                  />
                  <div>
                    <div>{match.team2.name}</div>
                    <small>{match.team2.players.join(' + ')}</small>
                  </div>
                </div>
              </div>
            ))}
          </section>

          <section style={{ display: 'flex', justifyContent: 'space-between', marginTop: 20 }}>
            <div style={{ flex: 1, marginRight: 10 }}>
              <h3 style={{ backgroundColor: '#b8860b', color: 'white', padding: 8, borderRadius: 4 }}>Bảng xếp hạng A</h3>
              {groupStandings.A.map((standing, idx) => (
                <div
                  key={standing.team.id}
                  style={{
                    backgroundColor: idx < 2 ? '#bfdbfe' : '#f3f4f6',
                    color: idx < 2 ? '#1e40af' : '#374151',
                    fontWeight: idx < 2 ? 'bold' : 'normal',
                    padding: 6,
                    borderRadius: 4,
                    marginTop: 4,
                    display: 'flex',
                    justifyContent: 'space-between',
                  }}
                >
                  <div>{idx + 1}. {standing.team.name} ({standing.team.players.join(' + ')})</div>
                  <div>{standing.wins}T - {standing.losses}B | HS: {standing.pointsDiff >= 0 ? '+' : ''}{standing.pointsDiff}</div>
                </div>
              ))}
            </div>

            <div style={{ flex: 1, marginLeft: 10 }}>
              <h3 style={{ backgroundColor: '#b8860b', color: 'white', padding: 8, borderRadius: 4 }}>Bảng xếp hạng B</h3>
              {groupStandings.B.map((standing, idx) => (
                <div
                  key={standing.team.id}
                  style={{
                    backgroundColor: idx < 2 ? '#bfdbfe' : '#f3f4f6',
                    color: idx < 2 ? '#1e40af' : '#374151',
                    fontWeight: idx < 2 ? 'bold' : 'normal',
                    padding: 6,
                    borderRadius: 4,
                    marginTop: 4,
                    display: 'flex',
                    justifyContent: 'space-between',
                  }}
                >
                  <div>{idx + 1}. {standing.team.name} ({standing.team.players.join(' + ')})</div>
                  <div>{standing.wins}T - {standing.losses}B | HS: {standing.pointsDiff >= 0 ? '+' : ''}{standing.pointsDiff}</div>
                </div>
              ))}
            </div>
          </section>

          {groupStandings.A.length >= 2 && groupStandings.B.length >= 2 && (
            <button
              onClick={generateKnockoutMatches}
