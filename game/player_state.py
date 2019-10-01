class PlayerState:
    def __init__(self, player, gameloop):
        self.player = player
        self.gameloop = gameloop
        self.summary = self.create_object_summary()

    def create_object_summary(self):
        if not self.player.collection_rate['minerals']:
            collection_rate = {
                'minerals': 0,
                'gas': 0,
            }

            unspent_resources = {
                'minerals': 0,
                'gas': 0,
            }
        else:
            collection_rate = {
                'minerals': self.player.collection_rate['minerals'][-1],
                'gas': self.player.collection_rate['gas'][-1],
            }

            unspent_resources = {
                'minerals': self.player.unspent_resources['minerals'][-1],
                'gas': self.player.unspent_resources['gas'][-1],
            }

        object_summary = {
            'gameloop': self.gameloop,
            'resource_collection_rate': collection_rate,
            'unspent_resources': unspent_resources,
            'unit': {},
            'building': {},
            'current_selection': {}
        }

        for obj in self.player.objects.values():
            worker = False
            for obj_type in obj.type:
                if obj_type == 'worker':
                    worker = True
                elif obj_type != 'supply':
                    if obj.name not in object_summary[obj_type]:
                        object_summary[obj_type][obj.name] = {
                            'type': [obj_type],
                            'live': 0,
                            'died': 0,
                            'in_progress': 0,
                            'mineral_cost': obj.mineral_cost,
                            'gas_cost': obj.gas_cost,
                        }

                    object_summary[obj_type][obj.name][obj.status] += 1
            if worker and 'worker' not in object_summary['unit'][obj.name]['type']:
                object_summary['unit'][obj.name]['type'].append('worker')

        for obj in self.player.current_selection:
            if obj.name not in object_summary['current_selection']:
                object_summary['current_selection'][obj.name] = 0
            object_summary['current_selection'][obj.name] += 1

        return object_summary
