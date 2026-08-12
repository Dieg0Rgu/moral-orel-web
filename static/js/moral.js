function openTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}

async function analizarVibras() {
    const situacion = document.getElementById('situacionInput').value;
    const resDiv = document.getElementById('vibrasResultados');
    resDiv.innerHTML = '<p>Buscando concordancia teológica...</p>';

    try {
        const response = await fetch('/api/vibras', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ situacion })
        });
        const data = await response.json();

        if (data.error) {
            resDiv.innerHTML = `<p style="color:red;">⚠️ ${data.error}</p>`;
            return;
        }

        resDiv.innerHTML = data.resultados.map(r => `
            <div class="quote-card">
                <p><strong>«${r.cita_es}»</strong></p>
                <p class="quote-en">Original: "${r.cita_en}"</p>
                <span class="author">— ${r.autor} (Afinidad: ${r.afinidad})</span>
            </div>
        `).join('');
    } catch (e) {
        resDiv.innerHTML = '<p style="color:red;">Error conectando con el servidor.</p>';
    }
}

async function generarDebate() {
    const pregunta = document.getElementById('preguntaInput').value;
    const resDiv = document.getElementById('polemistaResultado');
    resDiv.innerHTML = '<p>Redactando sermón apologético...</p>';

    try {
        const response = await fetch('/api/polemista', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta })
        });
        const data = await response.json();

        if (data.error) {
            resDiv.innerHTML = `<p style="color:red;">⚠️ ${data.error}</p>`;
            return;
        }

        resDiv.innerHTML = `
            <div class="sermon-text">${data.ensayo}</div>
            <p><small>Cita base original: "${data.cita_original}" por ${data.autor}</small></p>
        `;
    } catch (e) {
        resDiv.innerHTML = '<p style="color:red;">Error al generar el debate.</p>';
    }
}

async function procesarLotes() {
    const maxUnits = document.getElementById('maxUnits').value;
    const resDiv = document.getElementById('empaquetadorResultado');
    resDiv.innerHTML = '<p>Empaquetando oraciones y traduciendo en lotes...</p>';

    try {
        const response = await fetch('/api/empaquetador', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ max_units: maxUnits })
        });
        const data = await response.json();

        let html = `
            <div class="quote-card">
                <h3>Recibo de Optimización</h3>
                <p>Total de Citas Procesadas: <strong>${data.total_citas}</strong></p>
                <p>Total de Caracteres: <strong>${data.total_caracteres}</strong></p>
                <p>Peticiones HTTP (Lotes): <strong>${data.total_peticiones}</strong></p>
                <hr style="border-color: var(--border-color);">
                <h4>Desglose por Lotes:</h4>
                <ul>
        `;

        data.desglose.forEach(l => {
            html += `<li>Lote #${l.lote_num}: ${l.elementos} frases (${l.unidades} caracteres)</li>`;
        });

        html += '</ul></div>';
        resDiv.innerHTML = html;
    } catch (e) {
        resDiv.innerHTML = '<p style="color:red;">Error durante el proceso de empaquetado.</p>';
    }
}