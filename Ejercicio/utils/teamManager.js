// Gestor de la lógica de equipos
export class TeamManager {
    constructor(apiService, uiManager) {
        this.apiService = apiService;
        this.uiManager = uiManager;
        this.teams = [];
        this.filteredTeams = [];
        this.currentCountry = '';
        this.currentView = 'grid';
        this.searchTerm = '';
    }

    async loadTeams(country) {
        if (!country) return;
        
        this.currentCountry = country;
        this.uiManager.showLoading(true);
        this.uiManager.updateCountryTitle(country);
        
        try {
            this.teams = await this.apiService.getTeamsByCountry(country);
            this.filteredTeams = [...this.teams];
            this.searchTerm = '';
            
            this.uiManager.displayTeams(this.filteredTeams, this.currentView);
            this.uiManager.updateCounters(this.filteredTeams.length, this.teams.length);
            
            this.uiManager.showNotification(
                `${this.teams.length} equipos cargados de ${country}`,
                'success'
            );
            
            // Ocultar jugadores si están visibles
            this.uiManager.hidePlayersSection();
            
        } catch (error) {
            console.error('Error cargando equipos:', error);
            this.uiManager.showNotification('Error al cargar los equipos', 'error');
            this.uiManager.displayTeams([], this.currentView);
        } finally {
            this.uiManager.showLoading(false);
        }
    }

    filterTeams(searchTerm) {
        this.searchTerm = searchTerm.toLowerCase().trim();
        
        if (!this.searchTerm) {
            this.filteredTeams = [...this.teams];
        } else {
            this.filteredTeams = this.teams.filter(team =>
                team.strTeam.toLowerCase().includes(this.searchTerm) ||
                (team.strLeague && team.strLeague.toLowerCase().includes(this.searchTerm)) ||
                (team.strStadium && team.strStadium.toLowerCase().includes(this.searchTerm))
            );
        }
        
        this.uiManager.displayTeams(this.filteredTeams, this.currentView);
        this.uiManager.updateCounters(this.filteredTeams.length);
    }

    switchView(viewType) {
        this.currentView = viewType;
        if (this.filteredTeams.length > 0) {
            this.uiManager.displayTeams(this.filteredTeams, viewType);
            this.uiManager.setViewButtons(viewType);
        }
    }

    getCurrentCountry() {
        return this.currentCountry;
    }

    clearTeams() {
        this.teams = [];
        this.filteredTeams = [];
        this.currentCountry = '';
        this.searchTerm = '';
        this.uiManager.displayTeams([], this.currentView);
        this.uiManager.updateCounters(0);
        this.uiManager.updateCountryTitle('');
    }
}