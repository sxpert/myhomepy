class WindowTab {
    constructor(mainwindow) {
        this.tab_label = 'generic_tab';
        this.main = mainwindow;
        this.initialize();
    }

    initialize() {
        this.main.register_tab (this);
    }

    generate_html() {
        var link = $('<a href="">'+this.tab_label+'</a>');
        var tab = this;
        link.click(function(event){
            event.preventDefault();
            var t=tab; 
            t.click(event); 
        });
        return link;
    }

    click(event) {
        console.log(this.tab_label+' clicked');
    }
}

class ConfigTab extends WindowTab {
    initialize() {
        this.tab_label = 'Configuration';
        super.initialize();
    }
}

class DashboardTab extends WindowTab {
    initialize() {
        this.tab_label = 'Dashboard';
        super.initialize();
    }
}

class MainWindow {
    constructor (tabs) {
        this.tabs = [];
        for(var t of tabs) {
            new t(this);
        }
        this.initialize();
    }

    initialize() {
        this.body = $('body');
        // find the header bar
        this.header = $('#header');
        if (!this.header.length) {
            // not found, add the header element
            this.header = this.generate_html();
            this.header.prependTo(this.body);
        }
    }

    generate_html() {
        var header_container = $('<div id="header">');
        var caption = $('<div class="caption">');
        header_container.append(caption);
        var tab_bar = $('<div class="tab-bar">');
        for (var t of this.tabs) {
            tab_bar.append(t.generate_html());
        }   
        header_container.append(tab_bar);
        return header_container;
    }

    register_tab(tab) {
        this.tabs.push (tab);
    }


}

function myHomePy_UI() {
    var ui = new MainWindow([
            ConfigTab,
            DashboardTab
        ]);                
    console.log (ui);
}
