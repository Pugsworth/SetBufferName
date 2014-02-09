import sublime, sublime_plugin, re;



class SetBufferNameCommand(sublime_plugin.WindowCommand):
	def run(self):
		view = self.window.active_view();

		settings = sublime.load_settings("SetBufferName.sublime-settings");
		self.bauto = settings.get("auto_prefix", False);
		self.prefix = settings.get("prefix", "-- [%s] %c");
		self.substitutions = settings.get("substitutions");

		if view.file_name() != None:
			sublime.status_message("Not a temporary buffer, cannot change name.");
			return False;

		# Authored by Dr. WritesCodeInAwfulBlocks (TODO: less awful)
		self.oldname = view.name();
		prefixformatted = self.prefix.replace("%s", self.get_syntax(view));
		prefixcaretregex = re.search("%c", prefixformatted);
		prefixcaretpos = prefixcaretregex != None and prefixcaretregex.start() or -1;
		prefixformatted = prefixformatted.replace("%c", "");
		bnameempty = view.name().strip() == "";

		name = None;
		if bnameempty:
			name = prefixformatted;
		else:
			name = self.oldname;

		panel = self.window.show_input_panel("Set Name:", name, self.done, self.change, self.cancel);
		if bnameempty and prefixcaretregex > -1:
			panel.sel().clear(); # Clear the default caret placement
			panel.sel().add(sublime.Region(prefixcaretpos));

	def done(self, input):
		self.change_name(self.window.active_view(), input);

	def change(self, input):
		self.change_name(self.window.active_view(), input);

	def cancel(self):
		self.change_name(self.window.active_view(), self.oldname);
		
	def get_syntax(self, view):
		reg = re.search("/([^/]+).tmLanguage", view.settings().get("syntax"));
		if reg != None:
			syntax = reg.group(1);
			if syntax in self.substitutions:
				return self.substitutions[syntax];

			return syntax;

		return "ERROR RETRIEVING SYNTAX"; # Can a syntax file not actually exist?

	def change_name(self, view, name):
		view.set_name(name);
