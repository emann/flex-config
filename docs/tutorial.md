# Tutorial
We'll use a simplified version of the `config.py` included in our 
[fastapi-serverless-cookiecutter](https://triaxtec.github.io/fastapi-serverless-cookiecutter/) for illustration.

!!!warning
    In the below example we use all of the sources that come with flex_config. If you want to use all of them, you have 
    to install optional dependencies. The easiest way is to `poetry install flex_config -E all`. If you only need specific 
    sources (not all), then look at the API docs for that particular source to see what if any optional dependency you need.
    
## Creating a FlexConfig

Everything is based around Pydantic's `BaseModel`, which we subclass and add fields to that are then populated from one or
more [ConfigSource]s. Generally you want to create *one* of these and load its details only at startup, then reuse the
same instance throughout the application.

```python hl_lines="4 37 41 43 45 46 51 62"
{!./config.py!}
```

In the highlighted code, we:

1. Import `construct_config, ConfigSchema` and the `ConfigSource`s that we want to use
2. Declare a private global instance called `_app_config`, defaulting to `None`.
3. Declare a function called `get_config`. This is how every other part of the app will get the config.
4. Use the global `_app_config` locally in our function.
5. Return the global `_app_config` if it's already been set. This prevents us re-loading the config.
6. If `_app_config` hasn't been set up yet, we construct a brand new instance of our `Config` class via [construct_config].
7. Return our loaded up config object.


## Loading Sources

### A `dict`
Now let's take a look at *where* we are loading the config from that ends up in `_app_config`.


```python hl_lines="32 33 34 51 53 54 59"
{!./config.py!}
```

We have some defaults set in the code itself. Here this is a simple `dict` which very intentionally conforms to the 
 [ConfigSource] Protocol which is required for anything passed into [construct_config]. If you have a lot of defaults, you
 may want to use a [YAMLSource] instead.
 
Sources passed into [load_sources] are loaded **in order**. So in our case, we pass in `default_config` first so that
 every source we load later overrides it.

### Environment Variables
We're including an [EnvSource] to load values from environment variables. Usually, this source is used to load
 just enough info to be able to load from other sources. In the case of our serverless applications (where this was 
 taken from), we load the "env" config value to tell us which environment this is running in (e.g. "dev"). You could
 load your entire application's config from [EnvSource] if you wanted to, say, load a bunch of stuff from AWS Secrets
 manager into environment variables at boot up.
```python hl_lines="4 51 55 59"
{!./config.py!}
```

### YAML (or JSON or TOML) Files
Next up is a [YAMLSource]. Commonly we use this to store local config when developing since setting up environment
 variables or SSM config is cumbersome for values that may change frequently. The pattern shown is the same for a 
 [JSONSource] or [TOMLSource] - a path to the respective type is passed in and the rest is handled for you. 

```python hl_lines="4 38 51 56 59"
{!./config.py!}
```

### Overriding
In this case, we're also allowing users to provide an "override" param which we will load last. This pattern makes
 testing and loading config for CLIs much easier.
```python hl_lines="15 26 30 31"
{!./config.py!}
```

### Dynamically loading sources
 Finally, we're going to advantage of the fact that we can pass in a callable that takes in the dictionry of compiled
 values so far and returns a [ConfigSource]. Our function checks which environment we're running in (based on the 
 values loaded from the sources we've loaded so far). If we're not running locally, we return an [AWSSource] and load
 the rest of our config from AWS SSM. In this case, we've stored the values in SSM under the prefix "app/env"
 (e.g. "app/dev") though there is no limit to the length of the prefix nor the number of AWS sources you can load from.
 If we are running locally, `get_ssm_params` just returns an empty dictionary as there is nothing more to load.
```python hl_lines="4 25 26 27 28 29 51 57 59"
{!./config.py!}
```

[construct_config]: construct_config.md
[ConfigSource]: ConfigSources/config_source.md
[JSONSource]: ConfigSources/FileSources/json_source.md
[TOMLSource]: ConfigSources/FileSources/toml_source.md
[YAMLSource]: ConfigSources/FileSources/yaml_source.md
[EnvSource]: ConfigSources/env_source.md
[superset of JSON]: https://yaml.org/spec/1.2/spec.html#id2759572
