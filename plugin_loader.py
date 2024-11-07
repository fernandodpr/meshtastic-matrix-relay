import os
import sys
import importlib.util
import hashlib
import subprocess
import yaml
from log_utils import get_logger

logger = get_logger(name="Plugins")
sorted_active_plugins = []

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if not os.path.isfile(config_path):
        logger.error(f"Configuration file not found: {config_path}")
        return {}
    with open(config_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration file: {e}")
            return {}

def clone_or_update_repo(repo_url, tag, plugins_dir):
    # Extract the repository name from the URL
    repo_name = os.path.splitext(os.path.basename(repo_url.rstrip('/')))[0]
    repo_path = os.path.join(plugins_dir, repo_name)
    if os.path.isdir(repo_path):
        try:
            subprocess.check_call(['git', '-C', repo_path, 'fetch'])
            subprocess.check_call(['git', '-C', repo_path, 'checkout', tag])
            subprocess.check_call(['git', '-C', repo_path, 'pull', 'origin', tag])
            logger.info(f"Updated repository {repo_name} to {tag}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error updating repository {repo_name}: {e}")
            logger.error(f"Please manually git clone the repository {repo_url} into {repo_path}")
            sys.exit(1)
    else:
        try:
            subprocess.check_call(['git', 'clone', '--branch', tag, repo_url], cwd=plugins_dir)
            logger.info(f"Cloned repository {repo_name} from {repo_url} at {tag}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error cloning repository {repo_name}: {e}")
            logger.error(f"Please manually git clone the repository {repo_url} into {repo_path}")
            sys.exit(1)
    # Install requirements if requirements.txt exists
    requirements_path = os.path.join(repo_path, 'requirements.txt')
    if os.path.isfile(requirements_path):
        try:
            # Use pip to install the requirements.txt
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
            logger.info(f"Installed requirements for plugin {repo_name}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error installing requirements for plugin {repo_name}: {e}")
            logger.error(f"Please manually install the requirements from {requirements_path}")
            sys.exit(1)

def load_plugins_from_directory(directory, recursive=False):
    plugins = []
    if os.path.isdir(directory):
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.py'):
                    plugin_path = os.path.join(root, filename)
                    module_name = "plugin_" + hashlib.md5(plugin_path.encode('utf-8')).hexdigest()
                    spec = importlib.util.spec_from_file_location(module_name, plugin_path)
                    plugin_module = importlib.util.module_from_spec(spec)
                    try:
                        spec.loader.exec_module(plugin_module)
                        if hasattr(plugin_module, 'Plugin'):
                            plugins.append(plugin_module.Plugin())
                        else:
                            logger.warning(f"{plugin_path} does not define a Plugin class.")
                    except Exception as e:
                        logger.error(f"Error loading plugin {plugin_path}: {e}")
            if not recursive:
                break
    else:
        logger.warning(f"Directory {directory} does not exist.")
    return plugins

def load_plugins():
    global sorted_active_plugins
    if sorted_active_plugins:
        return sorted_active_plugins

    config = load_config()

    # Import core plugins
    from plugins.health_plugin import Plugin as HealthPlugin
    from plugins.map_plugin import Plugin as MapPlugin
    from plugins.mesh_relay_plugin import Plugin as MeshRelayPlugin
    from plugins.ping_plugin import Plugin as PingPlugin
    from plugins.telemetry_plugin import Plugin as TelemetryPlugin
    from plugins.weather_plugin import Plugin as WeatherPlugin
    from plugins.help_plugin import Plugin as HelpPlugin
    from plugins.nodes_plugin import Plugin as NodesPlugin
    from plugins.drop_plugin import Plugin as DropPlugin
    from plugins.debug_plugin import Plugin as DebugPlugin

    # Initial list of core plugins
    plugins = [
        HealthPlugin(),
        MapPlugin(),
        MeshRelayPlugin(),
        PingPlugin(),
        TelemetryPlugin(),
        WeatherPlugin(),
        HelpPlugin(),
        NodesPlugin(),
        DropPlugin(),
        DebugPlugin(),
    ]

    # Load custom plugins (non-recursive)
    custom_plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins', 'custom')
    plugins.extend(load_plugins_from_directory(custom_plugins_dir, recursive=False))

    # Process and download community plugins
    community_plugins_config = config.get('community-plugins', {})
    community_plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins', 'community')

    for plugin_info in community_plugins_config.values():
        if plugin_info.get('active', False):
            repo_url = plugin_info.get('repository')
            tag = plugin_info.get('tag', 'master')
            if repo_url:
                clone_or_update_repo(repo_url, tag, community_plugins_dir)
            else:
                logger.error(f"Repository URL not specified for a community plugin")
                logger.error("Please specify the repository URL in config.yaml")
                sys.exit(1)

    # Load community plugins (recursive)
    plugins.extend(load_plugins_from_directory(community_plugins_dir, recursive=True))

    # Filter and sort active plugins by priority
    active_plugins = []
    for plugin in plugins:
        if plugin.config.get("active", False):
            plugin.priority = plugin.config.get("priority", plugin.priority)
            active_plugins.append(plugin)
            try:
                plugin.start()
            except Exception as e:
                logger.error(f"Error starting plugin {plugin}: {e}")

    sorted_active_plugins = sorted(active_plugins, key=lambda plugin: plugin.priority)
    return sorted_active_plugins
