terminate(pyenv)

if exist("pe", "var")
    terminate(pe)
end

clear classes

pyExec = 'C:\Users\mariu\Anaconda3\envs\ANFIS\python.exe';

pe = pyenv("ExecutionMode","OutOfProcess");
if pe.Status == 'NotLoaded' || pe.Status == 'Terminated'
    disp("Reloading enviroenemtn");
    pe = pyenv("ExecutionMode","OutOfProcess","Version", pyExec);
end

pyRoot = fileparts(pyExec);
disp(pyRoot);
p = getenv('PATH');
p = strsplit(p, ';');
addToPath = {
    pyRoot
    fullfile(pyRoot, 'Library', 'mingw-w64', 'bin')
    fullfile(pyRoot, 'Library', 'usr', 'bin')
    fullfile(pyRoot, 'Library', 'bin')
    fullfile(pyRoot, 'Scripts')
    fullfile(pyRoot, 'bin')
    fullfile(pwd, 'Python')
    fullfile(pwd, 'Python', 'anfis')
    fullfile(pwd, 'Python', 'vizualize')
    pwd
    };
p = [addToPath(:); p(:)];
p = unique(p, 'stable');
p = strjoin(p, ';');
setenv('PATH', p);

disp(addToPath);

py.list; % Call a Python function to load interpreter
pyenv

python_paths = {'' 
                fullfile(pwd, "Python")
                fullfile(pwd, "Python", 'anfis') 
                fullfile(pwd, "Python", 'vizualize')};

for i=1:length(python_paths)
    name = python_paths{i};
    if count(py.sys.path, name) == 0
      insert(py.sys.path, int32(0), name);
    end
end

modules = {'numpy' ,'torch'};

for i=1:length(modules)
    module_to_load = modules{i};
    disp(module_to_load);
    python_module_to_use = py.importlib.import_module(module_to_load);
%    py.importlib.reload(python_module_to_use);
end