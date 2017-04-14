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

class ResizeVBar {
    constructor(left, right, min_width_left_percent = undefined, min_width_right_percent = undefined){
        this.left = left;
        this.right = right;
        this.min_width_left_percent = min_width_left_percent;
        this.min_width_right_percent = min_width_right_percent;
    }
    generate_html(){
        var bar = document.createElement('div');
        bar.setAttribute('class','resize-bar');
        var resize_bar = this;
        this.mouse_down_handler = function(e){
                var b = resize_bar;
                b.mouse_down(e);
            };
        bar.addEventListener('mousedown', this.mouse_down_handler);
        this.bar = bar;
        return bar;
    }
    mouse_down(e){
        // compute the offset
        var b_rect = this.bar.getBoundingClientRect();
        this.delta_x = e.clientX - b_rect.x;
        this.width = b_rect.width;
        var parent_b_rect = this.bar.parentElement.getBoundingClientRect();
        this.parent_width = parent_b_rect.width;
        this.min_width_left = ((this.parent_width-this.width) * this.min_width_left_percent) / 100.0;
        this.min_width_right = ((this.parent_width-this.width) * this.min_width_right_percent) / 100.0;
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
        var left = this.left[0];
        var left_width = (e.clientX-this.delta_x);
        var right = this.right[0];
        var right_width = this.parent_width-(e.clientX-this.delta_x+this.width);

        if (left_width < this.min_width_left) {
            left_width = this.min_width_left;
            right_width = this.parent_width - left_width - this.width;
        }
        if (right_width < this.min_width_right) {
            right_width = this.min_width_right;
            left_width = this.parent_width - right_width - this.width;
        }

        left_width += 'px';
        right_width += 'px';
        left.style.width = left_width;
        right.style.width = right_width;
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
        this.detail = $('<div class="detail-container">');
        this.resize_bar = new ResizeVBar(this.tree, this.detail, 10, 65);
        var jqrb = $(this.resize_bar.generate_html());
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
