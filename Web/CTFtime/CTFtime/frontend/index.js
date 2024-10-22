const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname,  'public', 'home.html'));
});

app.get('/team/:id(.*)', async (req, res) => {
    const teamId = req.params.id;

    if (teamId.includes("../") || teamId.includes("..\\") || teamId.includes("%") || teamId.includes("\\")) {
        return res.status(403).send("Forbidden");
    }

    try {
        const response = await fetch(`http://backend:5000/team/${teamId}`);
        if (!response.ok)
            return res.status(404).send("Team Not Found");
        const json = await response.json();

        if (json.error) {
            return res.status(500).send(json.error);
        }

        res.send(formatTeamInfo(json));
    } catch (err) {
        res.status(500).send(err.toString());
    }
});


function formatTeamInfo(json) {
    return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Team Info</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { padding-top: 20px; }
                .team-info { padding: 20px; }
                .team-logo { width: 100px; border-radius: 50%; }
                .table { margin-top: 20px; }
                .home-button { margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="home-button">
                    <a href="/" class="btn btn-secondary">Home</a>
                </div>
                <div class="row">
                    <div class="col-12">
                        <h2>Team: ${json.name} (${json.primary_alias})</h2>
                        <img src="${json.logo && json.logo.length > 0 ? json.logo : 'https://ctftime.org/static/images/nologo.png'}" alt="Team logo" class="team-logo">
                        <ul>
                            <li><strong>Country:</strong> ${json.country}</li>
                            <li><strong>Academic:</strong> ${json.academic ? "Yes" : "No"}</li>
                            <li><strong>University:</strong> ${json.university}</li>
                            <li><strong>Website:</strong> <a href="${json.university_website}" target="_blank">${json.university_website}</a></li>
                            <li><strong>Aliases:</strong> ${json.aliases?.join(", ")}</li>
                        </ul>
                        <h3>Ratings over the years:</h3>
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Year</th>
                                    <th>Rating Place</th>
                                    <th>Organizer Points</th>
                                    <th>Rating Points</th>
                                    <th>Country Place</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${Object.entries(json.rating || {})
                                    .sort(([yearA], [yearB]) => yearB - yearA)
                                    .map(([year, rating]) => `
                                        <tr>
                                            <td>${year}</td>
                                            <td>${rating.rating_place || 'N/A'}</td>
                                            <td>${rating.organizer_points || 'N/A'}</td>
                                            <td>${rating.rating_points || 'N/A'}</td>
                                            <td>${rating.country_place || 'N/A'}</td>
                                        </tr>
                                    `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </body>
        </html>
    `;
}

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});

