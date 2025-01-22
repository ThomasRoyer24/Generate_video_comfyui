Comfy_node = {

#Motion component

    "Sine": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "amplitude",
            "feature_mode": "relative",
            "target": "Zoom",
            "amplitude": 1,
            "cycles": 1,
            "phase": 0,
            "reverse": false,
            "bias": 0,
            "cumulative": false
        },
        "class_type": "DepthflowMotionSine",
        "_meta": {
            "title": "🌊 Depthflow Motion Sine"
        }
    }''',

    "Cosine": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "amplitude",
            "feature_mode": "relative",
            "target": "Isometric",
            "amplitude": 1,
            "cycles": 1,
            "phase": 0,
            "reverse": false,
            "bias": 0,
            "cumulative": false
        },
        "class_type": "DepthflowMotionCosine",
        "_meta": {
            "title": "🌊 Depthflow Motion Cosine"
        }
    }''',

    "Linear": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "start",
            "feature_mode": "relative",
            "target": "Isometric",
            "start": 0,
            "end": 1,
            "low": 0,
            "high": 1,
            "exponent": 1,
            "reverse": false,
            "cumulative": false
        },
        "class_type": "DepthflowMotionLinear",
        "_meta": {
            "title": "🌊 Depthflow Motion Linear"
        }
    }''',

    "Exponential": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "base",
            "feature_mode": "relative",
            "target": "Isometric",
            "base": 2,
            "scale": 1,
            "reverse": false,
            "cumulative": false
        },
        "class_type": "DepthflowMotionExponential",
        "_meta": {
            "title": "🌊 Depthflow Motion Exponential"
        }
    }''',

    "Arc": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "start",
            "feature_mode": "relative",
            "target": "OffsetX",
            "start": -0.5,
            "middle": -0.25,
            "end": 1,
            "reverse": false,
            "cumulative": false
        },
        "class_type": "DepthflowMotionArc",
        "_meta": {
            "title": "🌊 Depthflow Motion Arc"
        }
    }''',

    "Target": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "value",
            "feature_mode": "relative",
            "target": "Height",
            "value": 0.2
        },
        "class_type": "DepthflowMotionSetTarget",
        "_meta": {
            "title": "🌊 Depthflow Motion Set Target"
        }
    }''',

# Motion preset

    "Circle": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.65,
            "reverse": false,
            "smooth": true,
            "phase_x": 0,
            "phase_y": 0,
            "phase_z": 0,
            "amplitude_x": 1,
            "amplitude_y": 1,
            "amplitude_z": 0,
            "static_value": 0.3
        },
        "class_type": "DepthflowMotionPresetCircle",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Circle"
        }
    }''',

    "Dolly": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.8,
            "reverse": false,
            "smooth": true,
            "loop": true,
            "depth": 0.5
        },
        "class_type": "DepthflowMotionPresetDolly",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Dolly"
        }
    }''',

    "Horizontal": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.8,
            "reverse": false,
            "loop": true,
            "smooth": true,
            "phase": 0,
            "steady_value": 0.3
        },
        "class_type": "DepthflowMotionPresetHorizontal",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Horizontal"
        }
    }''',

    "Vertical": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.8,
            "reverse": false,
            "loop": true,
            "smooth": true,
            "phase": 0,
            "steady_value": 0.3
        },
        "class_type": "DepthflowMotionPresetVertical",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Vertical"
        }
    }''',

    "Zoom": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.8,
            "reverse": false,
            "smooth": true,
            "phase": 0,
            "loop": false
        },
        "class_type": "DepthflowMotionPresetZoom",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Zoom"
        }
    }''',

    "Orbital": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.8,
            "reverse": false,
            "depth": 0.5
        },
        "class_type": "DepthflowMotionPresetOrbital",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Orbital"
        }
    }''',

    "DOF": ''',"3": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "dof_intensity",
            "feature_mode": "absolute",
            "dof_enable": true,
            "dof_start": 0.3,
            "dof_end": 1,
            "dof_exponent": 2,
            "dof_intensity": 1,
            "dof_quality": 16,
            "dof_directions": 16
        },
        "class_type": "DepthflowEffectDOF",
        "_meta": {
            "title": "🌊 Depthflow Effect DOF"
        }
    }''',

    "Vignette": ''',"3": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "vignette_intensity",
            "feature_mode": "relative",
            "vignette_enable": true,
            "vignette_intensity": 30,
            "vignette_decay": 0.8
        },
        "class_type": "DepthflowEffectVignette",
        "_meta": {
            "title": "🌊 Depthflow Effect Vignette"
        }
    }''',


# Musique workflow

    "Musique":''',"204": {
    "inputs": {
      "audio": "",
      "start_time": 0,
      "duration": 0
    },
    "class_type": "VHS_LoadAudioUpload",
    "_meta": {
      "title": "Load Audio (Upload)🎥🅥🅗🅢"
    }
  },
  "205": {
    "inputs": {
      "frame_rate": 30,
      "model": [
        "206",
        0
      ],
      "audio": [
        "204",
        0
      ]
    },
    "class_type": "AudioSeparatorSimple",
    "_meta": {
      "title": "Audio Separator | RyanOnTheInside"
    }
  },
  "206": {
    "inputs": {
      "model_name": "umxl"
    },
    "class_type": "DownloadOpenUnmixModel",
    "_meta": {
      "title": "Download Open Unmix Model | RyanOnTheInside"
    }
  },
  "207": {
    "inputs": {
      "amount": 0,
      "image": [
        "",
        0
      ]
    },
    "class_type": "RepeatImageBatch",
    "_meta": {
      "title": "RepeatImageBatch"
    }
  },
  "208": {
    "inputs": {
      "extraction_method": "amplitude_envelope",
      "frame_rate": 30,
      "frame_count": 0,
      "width": 512,
      "height": 512,
      "audio": [
        "205",
        1
      ]
    },
    "class_type": "AudioFeatureExtractor",
    "_meta": {
      "title": "Audio Feature & Extractor | RyanOnTheInside"
    }
  },
  "209": {
    "inputs": {
      "lower_threshold": 0.3,
      "upper_threshold": 1,
      "invert_output": false,
       "feature": [
        "208",
        0
      ]
    },
    "class_type": "FeatureRebase",
    "_meta": {
      "title": "Feature Rebase ⚡🅡🅞🅣🅘"
    }
  },
  "210": {
    "inputs": {
      "smoothing_type": "moving_average",
      "window_size": 5,
      "alpha": 0.3,
      "sigma": 1,
      "invert_output": false,
      "feature": [
        "209",
        0
      ]
    },
    "class_type": "FeatureSmoothing",
    "_meta": {
      "title": "FeatureMod Smoothing | RyanOnTheInside"
    }
  }'''
}