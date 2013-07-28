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
				if len(primitive.texcoordset)>0 and len(primitive.texcoord_indexset)>0: # TODO: fix the hack
					mesh = Povray.Mesh2(
						#Povray.Texture(Povray.Pigment(color=(0.4,0.5,0.6))),
						Povray.Texture("uv_mapping", Povray.Pigment(Povray.ImageMap("models/"+primitive.material.effect.diffuse.sampler.surface.image.path))),
						vertex_vectors=Povray.List([(self.unitmeter*v[0], self.unitmeter*v[1], -self.unitmeter*v[2]) for v in primitive.vertex]),
						face_indices=Povray.List([tuple(i) for i in primitive.vertex_index]),
						uv_vectors=Povray.List([tuple(i) for i in primitive.texcoordset[0]]), # TODO: fix the hack
						uv_indices=Povray.List([tuple(i) for i in primitive.texcoord_indexset[0]]) # TODO: fix the hack
					).write(file)
					materials.add(primitive.material)

		for material in materials:
			pass