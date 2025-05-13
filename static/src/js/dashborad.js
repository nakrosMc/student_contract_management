/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, useState, onWillUnmount, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


class DashboardProtectionWidget extends Component {
    async mount() {
        const widget = new DashboardProtection();
        const container = document.getElementById('dashboard-protection-widget');
        container.appendChild(widget.el);
    }
}

// Registrar el widget OWL en la vista
registry.category('views').add('DashboardProtectionWidget', DashboardProtectionWidget);