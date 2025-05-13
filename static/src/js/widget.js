/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, useState, onWillUnmount, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class DashboardProtection extends Component {
    constructor() {
        super(...arguments);
        this.state = useState({
            iframeUrl: "https://app.powerbi.com/viewr=eyJrIjoiN2UyZDUzZTUtMTZmMi00YjMwLWFlZTEtZTk2NzQ1NjJhZ[...]6IjBiMTgwYjAyLTIzMTUtNDBjMS05ZWIxLTY0MDk4N2FmNDRkYyIsImMiOjl9",  // URL dinámica aquí
        });
    }

    render() {
        return `
            <div>
                <iframe 
                    src="${this.state.iframeUrl}"
                    style="width:100%; height:100%; border:none;"
                    sandbox="allow-same-origin allow-scripts allow-forms">
                </iframe>
            </div>
        `;
    }
}

// Registrar el componente en Odoo
registry.category('views').add('DashboardProtection', DashboardProtection);
