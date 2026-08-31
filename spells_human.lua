return {
    ["Cure Wounds"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 2,
                power = -4,
                mp = 3,
                requirements = {
                    level = 7,
                    barr = 3000
                }
            },
            [2] = {
                range = 2,
                power = -6,
                mp = 3,
                requirements = {
                    skill = 3,
                    barr = 200
                }
            },
            [3] = {
                range = 2,
                power = -8,
                mp = 3,
                requirements = {
                    item = {
                        id = 430,
                        name = "Spirit's Powder",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Healing"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 2,
                power = -10,
                mp = 3,
                requirements = {
                    intelligence = 11
                }
            },
            [2] = {
                range = 2,
                power = -12,
                mp = 3,
                requirements = {
                    skill = 5,
                    barr = 300
                }
            },
            [3] = {
                range = 2,
                power = -14,
                mp = 3,
                requirements = {
                    item = {
                        id = 430,
                        name = "Spirit's Powder",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = 3,
                power = -16,
                mp = 3,
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Fireball"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 5,
                power = 5,
                mp = 3,
                requirements = {
                    intelligence = 12,
                    barr = 200
                }
            },
            [2] = {
                range = 5,
                power = 7,
                mp = 3,
                requirements = {
                    skill = 5,
                    barr = 700
                }
            },
            [3] = {
                range = 5,
                power = 10,
                mp = 3,
                requirements = {
                    item = {
                        id = 430,
                        name = "Spirit's Powder",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Protection"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 0,
                duration = 30,
                power = -10,
                mp = 3,
                requirements = {
                    level = 5,
                    quest = "Magic Recommendation (Head of Town)"
                }
            },
            [2] = {
                range = 0,
                duration = 35,
                power = -12,
                mp = 3,
                requirements = {
                    skill = 5,
                    barr = 600
                }
            },
            [3] = {
                range = 0,
                duration = 40,
                power = -16,
                mp = 3,
                requirements = {
                    item = {
                        id = 430,
                        name = "Spirit's Powder",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Reflection"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 0,
                duration = 5,
                power = -1,
                mp = 8,
                requirements = {
                    intelligence = 18,
                    skill = 20,
                    any = {{
                        barr = 2500
                    }, {
                        item = {
                            id = 64,
                            name = "Orcish Metal",
                            quantity = 25
                        }
                    }, {
                        item = {
                            id = 90,
                            name = "Stige Skin",
                            quantity = 15
                        }
                    }}
                }
            },
            [2] = {
                range = 0,
                duration = 5,
                power = -1,
                mp = 7,
                requirements = {
                    skill = 25,
                    barr = 500
                }
            },
            [3] = {
                range = 0,
                duration = 5,
                power = -1,
                mp = 7,
                requirements = {
                    item = {
                        id = 430,
                        name = "Spirit's Powder",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                duration = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Weakening"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 4,
                duration = 20,
                power = 1,
                mp = 16,
                requirements = {
                    intelligence = 32,
                    skill = 50,
                    barr = 1000,
                    any = {{
                        item = {
                            id = 403,
                            name = "Scorpion Tail",
                            quantity = 15
                        }
                    }, {
                        item = {
                            id = 404,
                            name = "Lizardman Plates",
                            quantity = 10
                        }
                    }}
                }
            },
            [2] = {
                range = 4,
                duration = 25,
                power = 1,
                mp = 16,
                requirements = {
                    skill = 55,
                    barr = 1000
                }
            },
            [3] = {
                range = 4,
                duration = 30,
                power = 1,
                mp = 16,
                requirements = {
                    item = {
                        id = 430,
                        name = "Spirit's Powder",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = 5,
                duration = 35,
                power = 1,
                mp = 16,
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Stone Attack"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 4,
                power = 8,
                mp = 5,
                requirements = {
                    level = 17,
                    intelligence = 20,
                    skill = 25,
                    item = {
                        id = 225,
                        name = "Flute Of Earth",
                        quantity = 1
                    }
                }
            },
            [2] = {
                range = 4,
                power = 10,
                mp = 5,
                requirements = {
                    skill = 30,
                    barr = 1200
                }
            },
            [3] = {
                range = 4,
                power = 14,
                mp = 5,
                requirements = {
                    item = {
                        id = 430,
                        name = "Spirit's Powder",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Water Attack"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 4,
                power = 18,
                mp = 12,
                requirements = {
                    level = 19,
                    intelligence = 24,
                    skill = 28,
                    item = {
                        id = 224,
                        name = "Flute Of Water",
                        quantity = 1
                    }
                }
            },
            [2] = {
                range = 4,
                power = 20,
                mp = 12,
                requirements = {
                    skill = 33,
                    barr = 3000
                }
            },
            [3] = {
                range = 4,
                power = 26,
                mp = 12,
                requirements = {
                    item = {
                        id = 430,
                        name = "Spirit's Powder",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Flame Arrow"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 4,
                power = 20,
                mp = 15,
                requirements = {
                    level = 20,
                    intelligence = 28,
                    skill = 33,
                    item = {
                        id = 223,
                        name = "Flute Of Fire",
                        quantity = 1
                    }
                }
            },
            [2] = {
                range = 4,
                power = 22,
                mp = 15,
                requirements = {
                    skill = 38,
                    barr = 3200
                }
            },
            [3] = {
                range = 4,
                power = 28,
                mp = 15,
                requirements = {
                    item = {
                        id = 430,
                        name = "Spirit's Powder",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Healing Wind"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 2,
                power = -8,
                mp = 12,
                requirements = {
                    level = 22,
                    intelligence = 31,
                    skill = 30,
                    item = {
                        id = 226,
                        name = "Flute Of Wind",
                        quantity = 1
                    }
                }
            },
            [2] = {
                range = 2,
                power = -10,
                mp = 12,
                requirements = {
                    skill = 35,
                    barr = 2500
                }
            },
            [3] = {
                range = 2,
                power = -12,
                mp = 12,
                requirements = {
                    item = {
                        id = 430,
                        name = "Spirit's Powder",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Meteor Strike"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 5,
                power = 24,
                mp = 18,
                requirements = {
                    intelligence = 32,
                    skill = 38,
                    barr = 3000
                }
            }
        }
    },
    ["Ice Storm"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 5,
                power = 28,
                mp = 21,
                requirements = {
                    intelligence = 36,
                    skill = 43,
                    barr = 5000
                }
            }
        }
    },
    ["Dragon Breath"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 5,
                power = 36,
                mp = 27,
                requirements = {
                    intelligence = 57,
                    skill = 53,
                    barr = 7000
                }
            }
        }
    },
    ["Frost Wind"] = {
        race = "Human",
        school = "Blue",
        levels = {
            [1] = {
                range = 5,
                power = 30,
                mp = 35,
                requirements = {
                    intelligence = 91,
                    skill = 100,
                    barr = 10000
                }
            }
        }
    },
    ["Flame Bolt"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = 4,
                power = 7,
                mp = 5,
                requirements = {
                    level = 7,
                    intelligence = 13,
                    barr = 200,
                    item = {{
                        id = 69,
                        name = "Leocrot Leather",
                        quantity = 5
                    }, {
                        id = 52,
                        name = "Copper Metal",
                        quantity = 3
                    }}
                }
            },
            [2] = {
                range = 4,
                power = 10,
                mp = 5,
                requirements = {
                    skill = 5,
                    barr = 1000
                }
            },
            [3] = {
                range = 5,
                power = 16,
                mp = 5,
                requirements = {
                    item = {
                        id = 429,
                        name = "Devil`s Blood",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Spirit Sword"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = 5,
                power = 10,
                mp = 7,
                requirements = {
                    level = 12,
                    intelligence = 16,
                    skill = 5,
                    barr = 500,
                    item = {
                        id = 64,
                        name = "Orcish Metal",
                        quantity = 30
                    }
                }
            },
            [2] = {
                range = 5,
                power = 13,
                mp = 7,
                requirements = {
                    skill = 10,
                    barr = 1500
                }
            },
            [3] = {
                range = 6,
                power = 20,
                mp = 7,
                requirements = {
                    item = {
                        id = 429,
                        name = "Devil`s Blood",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Poison Curse"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = "3``",
                duration = 40,
                power = 6,
                mp = 10,
                requirements = {
                    level = 15,
                    intelligence = 20,
                    skill = 10,
                    item = {{
                        id = 63,
                        name = "Stige Metal",
                        quantity = 3
                    }, {
                        id = 139,
                        name = "Swamp Beast Gem",
                        quantity = 1
                    }}
                }
            },
            [2] = {
                range = 3,
                duration = 45,
                power = 8,
                mp = 10,
                requirements = {
                    skill = 15,
                    barr = 3000
                }
            },
            [3] = {
                range = 3,
                duration = 50,
                power = 12,
                mp = 9,
                requirements = {
                    item = {
                        id = 429,
                        name = "Devil`s Blood",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                duration = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Confusion"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = 4,
                duration = 20,
                power = 1,
                mp = 12,
                requirements = {
                    intelligence = 20,
                    skill = 20,
                    any = {{
                        item = {
                            id = 64,
                            name = "Orcish Metal",
                            quantity = 25
                        }
                    }, {
                        item = {
                            id = 90,
                            name = "Stige Skin",
                            quantity = 15
                        }
                    }, {
                        barr = 2500
                    }}
                }
            },
            [2] = {
                range = 4,
                duration = 25,
                power = 1,
                mp = 12,
                requirements = {
                    skill = 25,
                    barr = 500
                }
            },
            [3] = {
                range = 4,
                duration = 30,
                power = 1,
                mp = 11,
                requirements = {
                    item = {
                        id = 429,
                        name = "Devil`s Blood",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                duration = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Blindness"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = 4,
                duration = 20,
                power = 1,
                mp = 16,
                requirements = {
                    intelligence = 25,
                    skill = 50,
                    barr = 1000,
                    any = {{
                        item = {
                            id = 403,
                            name = "Scorpion Tail",
                            quantity = 15
                        }
                    }, {
                        item = {
                            id = 404,
                            name = "Lizardman Plate",
                            quantity = 10
                        }
                    }}
                }
            },
            [2] = {
                range = 4,
                duration = 25,
                power = 1,
                mp = 16,
                requirements = {
                    skill = 55,
                    barr = 1000
                }
            },
            [3] = {
                range = 4,
                duration = 30,
                power = 1,
                mp = 15,
                requirements = {
                    item = {
                        id = 429,
                        name = "Devil`s Blood",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                duration = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Crystal Arrow"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = 4,
                power = 13,
                mp = 10,
                requirements = {
                    intelligence = 19,
                    barr = 2000
                }
            }
        }
    },
    ["Death Blow"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = 5,
                power = 16,
                mp = 12,
                requirements = {
                    intelligence = 22,
                    skill = 50,
                    barr = 4000
                }
            }
        }
    },
    ["Black Lightning"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    intelligence = 32,
                    item = {{
                        id = 293,
                        name = "Gazer Crystal",
                        quantity = 5
                    }, {
                        id = 193,
                        name = "Golem Piece",
                        quantity = 2
                    }}
                }
            }
        }
    },
    ["Explosion"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    intelligence = 28,
                    moral = -31,
                    barr = 7000
                }
            }
        }
    },
    ["Hellfire"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    intelligence = 65,
                    skill = 100,
                    moral = -50,
                    item = {
                        id = 139,
                        name = "Swamp Beast Gem",
                        quantity = 10
                    }
                }
            }
        }
    },
    ["Chain Lightning"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    intelligence = 110,
                    skill = 100,
                    moral = -50,
                    barr = 10000
                }
            }
        }
    },
    ["Zombie"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    intelligence = 120,
                    skill = 100,
                    item = {{
                        id = 5134,
                        name = "Drazil Livers",
                        quantity = 50
                    }, {
                        id = 5135,
                        name = "Horror Eye",
                        quantity = 70
                    }, {
                        id = 5136,
                        name = "Prism Crystal",
                        quantity = 80
                    }, {
                        id = 5248,
                        name = "Demented Hog Tusk",
                        quantity = 1
                    }, {
                        id = 429,
                        name = "Devil`s Blood",
                        quantity = 1
                    }}
                }
            }
        }
    },
    ["Brimstone"] = {
        race = "Human",
        school = "Black",
        levels = {
            [1] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    level = "?",
                    intelligence = "?",
                    skill = "?",
                    moral = "?",
                    item = {{
                        id = 5909,
                        name = "Scroll of Valour",
                        quantity = 100
                    }, {
                        id = 5989,
                        name = "Gold Pile",
                        quantity = 10
                    }}
                }
            }
        }
    },
    ["Light Arrow"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = 5,
                power = 9,
                mp = 8,
                requirements = {
                    level = 8,
                    intelligence = 14,
                    item = {{
                        id = 70,
                        name = "Tiger Leather",
                        quantity = 3
                    }, {
                        id = 73,
                        name = "Tiger Claw",
                        quantity = 2
                    }, {
                        id = 71,
                        name = "White Tiger Leather",
                        quantity = 1
                    }}
                }
            },
            [2] = {
                range = 6,
                power = 10,
                mp = 6,
                requirements = {
                    skill = 5,
                    barr = 1000
                }
            },
            [3] = {
                range = 7,
                power = 14,
                mp = 6,
                requirements = {
                    item = {
                        id = 428,
                        name = "Angel`s Tear",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Cure Poison"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = 5,
                power = 0,
                mp = 7,
                requirements = {
                    level = 10,
                    intelligence = 15,
                    skill = 5,
                    barr = 300,
                    item = {
                        id = 64,
                        name = "Orcish Metal",
                        quantity = 10
                    }
                }
            },
            [2] = {
                range = 6,
                power = 0,
                mp = 6,
                requirements = {
                    skill = 10,
                    barr = 1200
                }
            },
            [3] = {
                range = 7,
                power = 0,
                mp = 5,
                requirements = {
                    item = {
                        id = 428,
                        name = "Angel`s Tear",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                power = 0,
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Light Sword"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = 3,
                power = 15,
                mp = 10,
                requirements = {
                    level = 15,
                    intelligence = 20,
                    skill = 10,
                    moral = 4,
                    barr = 500,
                    item = {{
                        id = 78,
                        name = "Werewolf Jewel",
                        quantity = 3
                    }, {
                        id = 90,
                        name = "Stige Skin",
                        quantity = 2
                    }}
                }
            },
            [2] = {
                range = 4,
                power = 16,
                mp = 8,
                requirements = {
                    skill = 15,
                    barr = 3000
                }
            },
            [3] = {
                range = 5,
                power = 20,
                mp = 8,
                requirements = {
                    item = {
                        id = 428,
                        name = "Angel`s Tear",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = 6,
                power = 22,
                mp = 6,
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Giggling"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = 4,
                duration = 30,
                power = 1,
                mp = 12,
                requirements = {
                    intelligence = 20,
                    skill = 20,
                    any = {{
                        barr = 2500
                    }, {
                        item = {
                            id = 64,
                            name = "Orcish Metal",
                            quantity = 25
                        }
                    }, {
                        item = {
                            id = 90,
                            name = "Stige Skin",
                            quantity = 15
                        }
                    }}
                }
            },
            [2] = {
                range = 5,
                duration = 35,
                power = 1,
                mp = 11,
                requirements = {
                    skill = 25,
                    barr = 500
                }
            },
            [3] = {
                range = 6,
                duration = 40,
                power = 1,
                mp = 10,
                requirements = {
                    item = {
                        id = 428,
                        name = "Angel`s Tear",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                duration = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Slow"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = 4,
                duration = 20,
                power = 1,
                mp = 16,
                requirements = {
                    intelligence = 25,
                    skill = 50,
                    barr = 1000,
                    any = {{
                        item = {
                            id = 403,
                            name = "Scorpion Tail",
                            quantity = 15
                        }
                    }, {
                        item = {
                            id = 404,
                            name = "Lizardman Plate",
                            quantity = 10
                        }
                    }}
                }
            },
            [2] = {
                range = 5,
                duration = 25,
                power = 1,
                mp = 15,
                requirements = {
                    skill = 55,
                    barr = 1000
                }
            },
            [3] = {
                range = 6,
                duration = 30,
                power = 1,
                mp = 14,
                requirements = {
                    item = {
                        id = 428,
                        name = "Angel`s Tear",
                        quantity = 1
                    }
                }
            },
            [4] = {
                range = "?",
                duration = "?",
                power = "?",
                mp = "?",
                requirements = {
                    item = {
                        id = 320,
                        name = "Diamond Large",
                        quantity = 1
                    }
                }
            }
        }
    },
    ["Infernal Arrow"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = 5,
                power = 20,
                mp = 11,
                requirements = {
                    intelligence = 33,
                    barr = 2000
                }
            }
        }
    },
    ["Energy Bolt"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = 5,
                power = 24,
                mp = 12,
                requirements = {
                    intelligence = 32,
                    barr = 4000
                }
            }
        }
    },
    ["Death Globe"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = 5,
                power = 28,
                mp = 13,
                requirements = {
                    intelligence = 38,
                    item = {{
                        id = 293,
                        name = "Gazer Crystal",
                        quantity = 5
                    }, {
                        id = 193,
                        name = "Golem Piece",
                        quantity = 2
                    }}
                }
            }
        }
    },
    ["Iron Fist"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = 5,
                power = 32,
                mp = 14,
                requirements = {
                    intelligence = 44,
                    barr = 7000
                }
            }
        }
    },
    ["Fire Storm"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = 5,
                power = 32,
                mp = 55,
                requirements = {
                    intelligence = 110,
                    skill = 100,
                    moral = 31,
                    barr = 10000
                }
            }
        }
    },
    ["Dispel Aura"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = "?",
                power = "?",
                mp = "?",
                requirements = {
                    intelligence = 120,
                    skill = 100,
                    item = {{
                        id = 5134,
                        name = "Drazil Livers",
                        quantity = 50
                    }, {
                        id = 5135,
                        name = "Horror Eye",
                        quantity = 70
                    }, {
                        id = 5136,
                        name = "Prism Crystal",
                        quantity = 80
                    }, {
                        id = 5248,
                        name = "Demented Hog Tusk",
                        quantity = 1
                    }, {
                        id = 428,
                        name = "Angel`s Tear",
                        quantity = 1
                    }}
                }
            }
        }
    },
    ["Smite"] = {
        race = "Human",
        school = "White",
        levels = {
            [1] = {
                range = 4,
                power = 41,
                mp = 40,
                requirements = {
                    level = "?",
                    intelligence = "?",
                    skill = "?",
                    moral = "?",
                    item = {{
                        id = 5909,
                        name = "Scroll of Valour",
                        quantity = 100
                    }, {
                        id = 5989,
                        name = "Gold Pile",
                        quantity = 10
                    }}
                }
            }
        }
    }
}
