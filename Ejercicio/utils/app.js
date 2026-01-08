import { ApiService } from './apiService.js';
import { UIManager } from './uiManager.js';
import { TeamManager } from './teamManager.js';
import { PlayerManager } from './playerManager.js';

// Clase principal de la aplicación
class FootballApp {
    constructor() {
        this.apiService = new ApiService();
        this.uiManager = new UIManager();
        this.teamManager = new TeamManager(this.apiService, this.uiManager);
        this.playerManager = new PlayerManager(this.apiService, this.uiManager);
        
        this.init();
    }

    async init() {
        this.setupEventListeners();
        await this.loadInitialData();
    }

    setupEventListeners() {
        const elements = this.uiManager.elements;
        
        // Eventos del selector de país
        elements.countrySelect.addEventListener('change', () => {
            const country = elements.countrySelect.value;
            this.uiManager.enableLoadButton(!!country);
        });
        
        // Botón cargar equipos
        elements.loadTeamsBtn.addEventListener('click', () => {
            const country = elements.countrySelect.value;
            if (country) {
                this.teamManager.loadTeams(country);
            }
        });
        
        // Búsqueda de equipos
        elements.teamSearch.addEventListener('input', (e) => {
            this.teamManager.filterTeams(e.target.value);
        });
        
        // Cambiar vista
        elements.gridViewBtn.addEventListener('click', () => {
            this.teamManager.switchView('grid');
        });
        
        elements.listViewBtn.addEventListener('click', () => {
            this.teamManager.switchView('list');
        });
        
        // Refrescar equipos
        elements.refreshTeamsBtn.addEventListener('click', () => {
            const country = elements.countrySelect.value;
            if (country) {
                this.teamManager.loadTeams(country);
            }
        });
        
        // Cerrar jugadores
        elements.closePlayersBtn.addEventListener('click', () => {
            this.playerManager.hidePlayers();
        });
        
        // Delegación para selección de equipo (configurada en UIManager)
        this.uiManager.onTeamSelected = (teamId, teamName, teamBadge, teamLeague) => {
            this.playerManager.loadPlayers(teamId, teamName, teamBadge, teamLeague);
        };
    }

    async loadInitialData() {
        try {
            this.uiManager.showLoading(true);
            const countries = await this.apiService.getCountries();
            this.uiManager.populateCountrySelect(countries);
            this.uiManager.showNotification(`${countries.length} países cargados`, 'success');
        } catch (error) {
            console.error('Error cargando datos iniciales:', error);
            this.uiManager.showNotification('Error al cargar los países', 'error');
        } finally {
            this.uiManager.showLoading(false);
        }
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new FootballApp();
});