// Gestor de la lógica de jugadores
export class PlayerManager {
    constructor(apiService, uiManager) {
        this.apiService = apiService;
        this.uiManager = uiManager;
        this.currentPlayers = [];
        this.currentTeam = null;
    }

    async loadPlayers(teamId, teamName, teamBadge, teamLeague) {
        if (!teamId) return;
        
        this.uiManager.showLoading(true);
        
        try {
            const players = await this.apiService.getPlayersByTeam(teamId);
            this.currentPlayers = players;
            this.currentTeam = { name: teamName, badge: teamBadge, league: teamLeague };
            
            const country = this.uiManager.elements.countrySelect.value;
            this.uiManager.displayPlayers(players, teamName, teamBadge, teamLeague, country);
            
            this.uiManager.showNotification(
                `${players.length} jugadores cargados`,
                'success'
            );
            
        } catch (error) {
            console.error('Error cargando jugadores:', error);
            this.uiManager.showNotification('Error al cargar los jugadores', 'error');
            this.uiManager.displayPlayers([], teamName, teamBadge, teamLeague);
        } finally {
            this.uiManager.showLoading(false);
        }
    }

    hidePlayers() {
        this.currentPlayers = [];
        this.currentTeam = null;
        this.uiManager.hidePlayersSection();
    }

    getCurrentTeam() {
        return this.currentTeam;
    }

    getPlayerCount() {
        return this.currentPlayers.length;
    }
}