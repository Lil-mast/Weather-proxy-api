// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    const tabsContainer = document.getElementById('tabs-container');
    const citySearchInput = document.getElementById('city-search-input');

    // --- STATE MANAGEMENT ---
    let currentCity = 'Nairobi'; // Default city

    // --- API FETCHING ---
    const fetchData = async (endpoint, city) => {
        const url = `/api/weather/${endpoint}/?city=${city}`;
        try {
            const response = await fetch(url);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Failed to fetch ${endpoint}:`, error);
            // Display error in a user-friendly way
            const todayContent = document.getElementById('tab-content-today');
            todayContent.innerHTML = `<p class="text-red-400 p-4">${error.message}</p>`;
            return null;
        }
    };

    // --- UI RENDERING ---

    const renderTabs = (activeTabId) => {
        const tabs = [
            { id: 'today', label: 'Today', icon: '<svg>...</svg>' /* Add SVG paths */ },
            { id: 'forecast', label: 'Forecast', icon: '<svg>...</svg>' },
            { id: 'map', label: 'Weather Map', icon: '<svg>...</svg>' },
            { id: 'details', label: 'Details & Health', icon: '<svg>...</svg>' },
        ];
        // For brevity, SVG paths are omitted. Copy them from the original HTML if needed.

        tabsContainer.innerHTML = tabs.map(tab => `
            <a href="#" class="tab-link flex flex-col items-center justify-center border-b-[3px] text-[#9cbaaf] gap-1 pb-[7px] pt-2.5 flex-1 ${tab.id === activeTabId ? 'active' : ''}" data-tab="${tab.id}">
                <p class="text-sm font-bold leading-normal">${tab.label}</p>
            </a>
        `).join('');
    };

    const renderTodayContent = (data) => {
        const container = document.getElementById('tab-content-today');
        container.innerHTML = `
            <div class="w-full bg-center bg-no-repeat bg-cover flex flex-col justify-end overflow-hidden rounded-xl min-h-[218px]" style="background-image: url('https://source.unsplash.com/800x400/?${data.location.city}')"></div>
            <h1 class="text-white tracking-light text-[32px] font-bold leading-tight px-4 text-left pb-3 pt-6">${data.location.city}, ${data.location.country}</h1>
            <h1 class="text-white tracking-light text-[32px] font-bold leading-tight px-4 text-left pb-3 pt-6">${Math.round(data.weather.temperature_celsius)}°C</h1>
            <p class="text-white text-base font-normal leading-normal pb-3 pt-1 px-4">${data.weather.description}</p>
            <p class="text-white text-base font-normal leading-normal pb-3 pt-1 px-4">H: ${Math.round(data.weather.temp_high_celsius)}°C L: ${Math.round(data.weather.temp_low_celsius)}°C</p>
        `;
    };
    
    const renderDetailsContent = (data) => {
        const container = document.getElementById('tab-content-details');
        container.innerHTML = `
            <h2 class="text-white text-[22px] font-bold leading-tight px-4 pb-3 pt-5">Details &amp; Health</h2>
            <div class="p-4 grid grid-cols-2">
              <div class="flex flex-col gap-1 border-t border-solid border-t-[#3b544b] py-4 pr-2">
                <p class="text-[#9cbaaf] text-sm">Humidity</p>
                <p class="text-white text-sm">${data.weather.humidity_percent}%</p>
              </div>
              <div class="flex flex-col gap-1 border-t border-solid border-t-[#3b544b] py-4 pl-2">
                <p class="text-[#9cbaaf] text-sm">Wind</p>
                <p class="text-white text-sm">${data.weather.wind_speed_ms.toFixed(1)} m/s</p>
              </div>
              <!-- Placeholder for data not yet in API -->
              <div class="flex flex-col gap-1 border-t border-solid border-t-[#3b544b] py-4 pr-2">
                <p class="text-[#9cbaaf] text-sm">UV Index</p> <p class="text-white text-sm">Moderate</p>
              </div>
              <div class="flex flex-col gap-1 border-t border-solid border-t-[#3b544b] py-4 pl-2">
                <p class="text-[#9cbaaf] text-sm">Air Quality</p> <p class="text-white text-sm">Good</p>
              </div>
            </div>
        `;
    };

    const renderForecastContent = (data) => {
        const container = document.getElementById('tab-content-forecast');
        container.innerHTML = `
            <h2 class="text-white text-[22px] font-bold leading-tight px-4 pb-3 pt-5">5-Day Forecast</h2>
            <div class="flex flex-col p-4 gap-3">
                ${data.map(day => `
                    <div class="flex items-center justify-between p-2 rounded-lg hover:bg-[#283933]">
                        <p class="text-white text-base font-medium w-1/4">${day.day_of_week}</p>
                        <img src="${day.icon_url}" alt="${day.description}" class="w-10 h-10">
                        <p class="text-[#9cbaaf] text-sm w-1/4 text-center">${day.description}</p>
                        <p class="text-white text-base font-medium w-1/4 text-right">${Math.round(day.temp_high)}° / ${Math.round(day.temp_low)}°</p>
                    </div>
                `).join('')}
            </div>
        `;
    };


    // --- EVENT HANDLING ---

    const switchTab = (tabId) => {
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        document.getElementById(`tab-content-${tabId}`).classList.add('active');
        renderTabs(tabId);
    };

    tabsContainer.addEventListener('click', (e) => {
        const link = e.target.closest('.tab-link');
        if (link) {
            e.preventDefault();
            const tabId = link.dataset.tab;
            switchTab(tabId);
        }
    });

    citySearchInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            const newCity = e.target.value.trim();
            if (newCity) {
                currentCity = newCity;
                loadAllWeatherData();
                e.target.value = ''; // Clear input
            }
        }
    });

    // --- INITIALIZATION ---
    
    const loadAllWeatherData = async () => {
        // Show a loading state
        document.getElementById('tab-content-today').innerHTML = `<p class="text-white p-4">Loading weather for ${currentCity}...</p>`;
        
        const currentData = await fetchData('current', currentCity);
        const forecastData = await fetchData('forecast', currentCity);

        if (currentData) {
            renderTodayContent(currentData);
            renderDetailsContent(currentData);
        }
        if (forecastData) {
            renderForecastContent(forecastData);
        }
    };

    // Initial load
    switchTab('today');
    loadAllWeatherData();
});