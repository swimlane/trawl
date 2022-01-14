from spotter import Spotter


spotter = Spotter()
for service in ['phishingdatabase', 'openphish', 'phishtank']:
    spotter.run(service)
