import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib import animation, rc
rc('animation', html='html5', writer='avconv')

def minimize_poly(poly, starting_point, tol = 1e-5, lr=0.01):
	poly_deriv = poly.deriv()
	point_coords = [starting_point]
	df=np.inf
	while abs(df)>tol:
		point_coords.append(point_coords[-1]-lr*poly_deriv(point_coords[-1]))
		df = poly(point_coords[-1])-poly(point_coords[-2])

	return point_coords

def animate_poly_minimization(poly, x, starting_point):
	point_coords = minimize_poly(poly, starting_point)

	fig, ax = plt.subplots()
	ax.plot(x, poly(x))
	point, = ax.plot([],[],'bo', color='red',markersize=10)

	def init():
		point.set_data([],[])
		return point,

	def animate(i):
		point.set_data(point_coords[i],poly(point_coords[i]) )
		return point,

	anim = animation.FuncAnimation(fig, animate, init_func=init,
								   frames=len(point_coords), interval=20, blit=True)
	plt.close()
	return anim
	
def animate_poly_minimization_with_slope(poly, x, starting_point):
	poly_deriv = poly.deriv()
	point_coords = minimize_poly(poly, starting_point)
	fig, ax = plt.subplots()
	ax.plot(x, poly(x))
	point, = ax.plot([],[],'bo', color='red',markersize=10)

	arrow = None

	def tangent(p):
		der = poly_deriv(p)
		return np.polynomial.Polynomial([poly(p)-der*p, der])

	def init():
		point.set_data([],[])
		return point,

	def animate(i):
		p = point_coords[i]
		point.set_data(p,poly(p))
		
		global arrow
		if i!=0:
			ax.patches.remove(arrow) 
		
		tang = tangent(p)
		step = 0.5*poly_deriv(p)
		ps = [p+step, p-step]
		arrow = plt.Arrow(ps[0], tang(ps[0]), ps[1]-ps[0], tang(ps[1])-tang(ps[0]), color='red', width = 0.3)
		ax.add_patch(arrow)
		return point, arrow

	anim = animation.FuncAnimation(fig, animate, init_func=init,
								   frames=len(point_coords), interval=20, blit=True)
	plt.close()
	return anim