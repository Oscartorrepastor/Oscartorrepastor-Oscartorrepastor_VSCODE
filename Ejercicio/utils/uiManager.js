// Gestor de la interfaz de usuario
export class UIManager {
    constructor() {
        this.elements = this.cacheElements();
        this.setupEventDelegation();
    }

    cacheElements() {
        return {
            // Selectores
            countrySelect: document.getElementById('countrySelect'),
            loadTeamsBtn: document.getElementById('loadTeamsBtn'),
            teamSearch: document.getElementById('teamSearch'),
            teamsContainer: document.getElementById('teamsContainer'),
            playersContainer: document.getElementById('playersContainer'),
            playersSection: document.getElementById('playersSection'),
            teamInfo: document.getElementById('teamInfo'),
            emptyPlayers: document.getElementById('emptyPlayers'),
            
            // Contadores
            teamsCount: document.getElementById('teamsCount'),
            countryTitle: document.getElementById('countryTitle'),
            playersTitle: document.getElementById('playersTitle'),
            totalTeams: document.getElementById('totalTeams'),
            
            // Botones
            gridViewBtn: document.getElementById('gridViewBtn'),
            listViewBtn: document.getElementById('listViewBtn'),
            refreshTeamsBtn: document.getElementById('refreshTeamsBtn'),
            closePlayersBtn: document.getElementById('closePlayersBtn'),
            
            // Info equipo
            teamBadge: document.getElementById('teamBadge'),
            teamName: document.getElementById('teamName'),
            teamDetails: document.getElementById('teamDetails'),
            
            // Loading
            loadingOverlay: document.getElementById('loadingOverlay'),
            notification: document.getElementById('notification')
        };
    }

    setupEventDelegation() {
        // Delegación de eventos para botones dinámicos
        document.addEventListener('click', (e) => {
            const teamCard = e.target.closest('.team-card');
            if (teamCard) {
                const viewBtn = teamCard.querySelector('.view-players-btn');
                if (viewBtn && (e.target === viewBtn || e.target.closest('.view-players-btn'))) {
                    const teamId = viewBtn.dataset.teamId;
                    const teamName = viewBtn.dataset.teamName;
                    const teamBadge = viewBtn.dataset.teamBadge;
                    const teamLeague = viewBtn.dataset.teamLeague;
                    
                    if (teamId && this.onTeamSelected) {
                        this.onTeamSelected(teamId, teamName, teamBadge, teamLeague);
                    }
                }
            }
        });
    }

    populateCountrySelect(countries) {
        this.elements.countrySelect.innerHTML = '<option value="" disabled selected>Selecciona un país</option>';
        
        countries.sort((a, b) => a.name_en.localeCompare(b.name_en)).forEach(country => {
            const option = document.createElement('option');
            option.value = country.name_en;
            option.textContent = country.name_en;
            this.elements.countrySelect.appendChild(option);
        });
    }

    displayTeams(teams, viewType = 'grid') {
        this.elements.teamsContainer.innerHTML = '';
        
        if (teams.length === 0) {
            this.elements.teamsContainer.innerHTML = `
                <div class="col-12 text-center py-5">
                    <p class="text-muted">No se encontraron equipos</p>
                </div>
            `;
            return;
        }

        teams.forEach(team => {
            const teamCard = this.createTeamCard(team, viewType);
            this.elements.teamsContainer.appendChild(teamCard);
        });
    }

    createTeamCard(team, viewType) {
        const col = document.createElement('div');
        
        if (viewType === 'grid') {
            col.className = 'col-md-6 col-lg-4 col-xl-3 mb-4';
            col.innerHTML = this.createGridCard(team);
        } else {
            col.className = 'col-12 mb-3';
            col.innerHTML = this.createListCard(team);
        }
        
        return col;
    }

    createGridCard(team) {
        return `
            <div class="card team-card h-100">
                <div class="card-img-top p-3 text-center bg-light" style="height: 150px;">
                    <img src="${team.strTeamBadge || 'https://via.placeholder.com/100x100?text=No+logo'}" 
                         alt="${team.strTeam}" 
                         class="img-fluid h-100"
                         onerror="this.src='https://via.placeholder.com/100x100?text=No+logo'">
                </div>
                <div class="card-body d-flex flex-column">
                    <h6 class="card-title">${team.strTeam}</h6>
                    ${team.strLeague ? `<p class="card-text"><small class="text-muted">${team.strLeague}</small></p>` : ''}
                    ${team.strStadiumLocation ? `<p class="card-text"><small>🏟️ ${team.strStadiumLocation}</small></p>` : ''}
                    <button class="btn btn-primary btn-sm mt-auto view-players-btn"
                            data-team-id="${team.idTeam}"
                            data-team-name="${team.strTeam}"
                            data-team-badge="${team.strTeamBadge}"
                            data-team-league="${team.strLeague || ''}">
                        👥 Ver Plantilla
                    </button>
                </div>
            </div>
        `;
    }

    createListCard(team) {
        return `
            <div class="card team-card">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-auto">
                            <img src="${team.strTeamBadge || 'https://via.placeholder.com/50x50?text=No+logo'}" 
                                 alt="${team.strTeam}" 
                                 class="img-thumbnail"
                                 style="width: 50px;"
                                 onerror="this.src='https://via.placeholder.com/50x50?text=No+logo'">
                        </div>
                        <div class="col">
                            <h6 class="mb-1">${team.strTeam}</h6>
                            <div class="text-muted">
                                ${team.strLeague ? `<small class="me-2">🏆 ${team.strLeague}</small>` : ''}
                                ${team.intFormedYear ? `<small>📅 ${team.intFormedYear}</small>` : ''}
                            </div>
                        </div>
                        <div class="col-auto">
                            <button class="btn btn-primary btn-sm view-players-btn"
                                    data-team-id="${team.idTeam}"
                                    data-team-name="${team.strTeam}"
                                    data-team-badge="${team.strTeamBadge}"
                                    data-team-league="${team.strLeague || ''}">
                                👥 Plantilla
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    displayPlayers(players, teamName, teamBadge, teamLeague, country) {
        // Mostrar info del equipo
        this.elements.teamInfo.style.display = 'flex';
        this.elements.teamBadge.src = teamBadge || 'https://via.placeholder.com/50x50?text=Team';
        this.elements.teamBadge.alt = teamName;
        this.elements.teamName.textContent = teamName;
        this.elements.teamDetails.textContent = `${teamLeague || 'Sin liga'} • ${country}`;
        
        // Actualizar título
        this.elements.playersTitle.textContent = `Plantilla: ${teamName}`;
        
        // Limpiar contenedor
        this.elements.playersContainer.innerHTML = '';
        
        if (players.length === 0) {
            this.elements.emptyPlayers.style.display = 'block';
            return;
        }
        
        this.elements.emptyPlayers.style.display = 'none';
        
        // Crear cards de jugadores
        players.forEach(player => {
            const playerCard = this.createPlayerCard(player);
            this.elements.playersContainer.appendChild(playerCard);
        });
        
        // Mostrar sección
        this.elements.playersSection.style.display = 'block';
        this.elements.playersSection.scrollIntoView({ behavior: 'smooth' });
    }

    createPlayerCard(player) {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4 mb-3';
        
        col.innerHTML = `
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex align-items-start mb-2">
                        <div class="me-3">
                            <img src="${player.strCutout || player.strThumb || 'https://via.placeholder.com/50x50?text=Jugador'}" 
                                 alt="${player.strPlayer}" 
                                 class="img-thumbnail"
                                 style="width: 60px; height: 60px; object-fit: cover;"
                                 onerror="this.src='https://via.placeholder.com/50x50?text=Jugador'">
                        </div>
                        <div class="flex-grow-1">
                            <h6 class="card-title mb-1">${player.strPlayer}</h6>
                            ${player.strPosition ? `<p class="card-text mb-1"><small>⚽ ${player.strPosition}</small></p>` : ''}
                            ${player.strNationality ? `<p class="card-text mb-1"><small>🌍 ${player.strNationality}</small></p>` : ''}
                        </div>
                    </div>
                    ${player.dateBorn ? `<p class="card-text"><small>🎂 ${new Date(player.dateBorn).toLocaleDateString('es-ES')}</small></p>` : ''}
                    ${player.strSigning ? `<p class="card-text"><small>💰 ${player.strSigning}</small></p>` : ''}
                </div>
            </div>
        `;
        
        return col;
    }

    updateCounters(teamsCount, totalTeams = null) {
        this.elements.teamsCount.textContent = `${teamsCount} equipos`;
        if (totalTeams !== null) {
            this.elements.totalTeams.textContent = totalTeams;
        }
    }

    updateCountryTitle(country) {
        this.elements.countryTitle.textContent = country ? `Equipos de ${country}` : 'Equipos';
    }

    showLoading(show) {
        this.elements.loadingOverlay.classList.toggle('d-none', !show);
        this.elements.loadingOverlay.classList.toggle('d-flex', show);
    }

    showNotification(message, type = 'info') {
        const toastId = 'toast-' + Date.now();
        const toastEl = document.createElement('div');
        
        let bgClass = 'bg-primary';
        if (type === 'error') bgClass = 'bg-danger';
        if (type === 'success') bgClass = 'bg-success';
        
        toastEl.className = `toast ${bgClass} text-white`;
        toastEl.setAttribute('role', 'alert');
        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        this.elements.notification.appendChild(toastEl);
        const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
        toast.show();
        
        toastEl.addEventListener('hidden.bs.toast', () => {
            toastEl.remove();
        });
    }

    hidePlayersSection() {
        this.elements.playersSection.style.display = 'none';
        this.elements.teamInfo.style.display = 'none';
        this.elements.emptyPlayers.style.display = 'none';
    }

    setViewButtons(activeView) {
        this.elements.gridViewBtn.classList.toggle('active', activeView === 'grid');
        this.elements.listViewBtn.classList.toggle('active', activeView === 'list');
    }

    enableLoadButton(enable) {
        this.elements.loadTeamsBtn.disabled = !enable;
    }
}