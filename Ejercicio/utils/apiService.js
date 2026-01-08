// Servicio para manejar todas las llamadas a la API
export class ApiService {
    constructor() {
        this.API_BASE = 'https://www.thesportsdb.com/api/v1/json/123';
    }

    async getCountries() {
        try {
            const response = await fetch(`${this.API_BASE}/all_countries.php`);
            if (!response.ok) throw new Error('Error al cargar países');
            const data = await response.json();
            return data.countries || [];
        } catch (error) {
            console.error('Error en getCountries:', error);
            throw error;
        }
    }

    async getTeamsByCountry(country) {
        try {
            const response = await fetch(`${this.API_BASE}/search_all_teams.php?s=Soccer&c=${encodeURIComponent(country)}`);
            if (!response.ok) throw new Error('Error al cargar equipos');
            const data = await response.json();
            return data.teams || [];
        } catch (error) {
            console.error('Error en getTeamsByCountry:', error);
            throw error;
        }
    }

    async getPlayersByTeam(teamId) {
        try {
            const response = await fetch(`${this.API_BASE}/lookup_all_players.php?id=${teamId}`);
            if (!response.ok) throw new Error('Error al cargar jugadores');
            const data = await response.json();
            return data.player || [];
        } catch (error) {
            console.error('Error en getPlayersByTeam:', error);
            throw error;
        }
    }
}