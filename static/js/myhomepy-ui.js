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
        this.main.set_window(this.config_window)
    }
}

class ConfigTab extends WindowTab {
    initialize() {
        this.tab_label = 'Configuration';
        this.config_window = new ConfigWindow();
        super.initialize();
    }
}

class ResizeBar {
    constructor(){
        console.log('resizer-bar constructor');
    }
    generate_html(){
        var bar = document.createElement('div');
        bar.setAttribute('class','resize-bar');
        var resize_bar = this;
        this.mouse_down_handler = function(e){
                var b = resize_bar;
                console.log(b);
                b.mouse_down(e);
            };
        bar.addEventListener('mousedown', this.mouse_down_handler);
        this.bar = bar;
        return bar;
    }
    mouse_down(e){
        e.target.setCapture(true);
        var resize_bar = this;
        this.mouse_move_handler = function(e){
                var b = resize_bar;
                b.mouse_move(e);
            };
        e.target.addEventListener('mousemove', this.mouse_move_handler);
        this.mouse_up_handler = function(e){
                var b = resize_bar;
                b.mouse_up(e);
            };
        e.target.addEventListener('mouseup', this.mouse_up_handler);
    }
    mouse_move(e){
        console.log(e.clientX+' '+e.clientY);
    }
    mouse_up(e){
        e.target.removeEventListener('mousemove', this.mouse_move_handler);
        e.target.removeEventListener('mouseup', this.mouse_up_handler);
        document.releaseCapture();
    }
}

class ConfigWindow {
    constructor() {
        console.log('Configuration window created');
    }
    generate_html() {
        this.tree = $('<div class="options-tree">');
        this.resize_bar = new ResizeBar();
        var jqrb = $(this.resize_bar.generate_html());
        this.detail = $('<div class="detail-container">');
        var subwindows = [
            this.tree,
            jqrb,
            this.detail
        ];
        return subwindows;
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

    set_window(window) {
        this.active_window = window;
        console.log(this.active_window);
        if (this.window_container === undefined) {
            this.window_container = $('<div id="main">');
            this.window_container.appendTo(this.body);
        }
        var contents = this.window_container.children();
        console.log('contents', contents);
        if (contents.length > 0) {
            contents.remove();
        }
        this.window_container.append(this.active_window.generate_html());
    }
}

function myHomePy_UI() {
    var ui = new MainWindow([
            ConfigTab,
            DashboardTab
        ]);                
    console.log (ui);
}
