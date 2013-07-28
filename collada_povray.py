#!/usr/bin/env python

import collada, pypov.Povray as Povray

class ColladaPovray():
	
	model = None
	unitmeter = 1

	def __init__(self, filename):
		model = collada.Collada(filename, ignore=[collada.DaeUnsupportedError, collada.DaeBrokenRefError])
		self.model = model
		assetInfo = model.assetInfo
		if hasattr(assetInfo, "unitmeter"):
			self.unitmeter = float(assetInfo.unitmeter)

	def convert(self):
		file = Povray.File("out.pov","colors.inc","axis.pov")
		Povray.Camera(
			location=(-2,10,-7),
			look_at=(0,0,0)
		).write(file)
		Povray.LightSource(
			(100,300,-200),
			color="White"
		).write(file)

		model = self.model
		materials = set()
		# iterating through bounded geometries
		for geometry in model.scene.objects("geometry"):
			for primitive in geometry.primitives():
				mesh = Povray.Mesh2(
					Povray.Texture(Povray.Pigment(color=(0.4,0.5,0.6))),
					vertex_vectors=Povray.List([(self.unitmeter*v[0], self.unitmeter*v[1], -self.unitmeter*v[2]) for v in primitive.vertex]),
					face_indices=Povray.List([tuple(i) for i in primitive.vertex_index])
				).write(file)
				materials.add(primitive.material)

		for material in materials:
			pass
			#if mat:inspectMaterial( mat )