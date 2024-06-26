from pytest import approx
import numpy as np

from maxwell.dg.dg2d_tools import *
from maxwell.dg.mesh2d import *

TEST_DATA_FOLDER = 'testData/'


def test_set_nodes_N1():
    x, y = set_nodes_in_equilateral_triangle(1)
    assert np.allclose(np.array([-1.0, 1.0, 0.0]), x, rtol=1e-3)
    assert np.allclose(
        np.array([-1/np.sqrt(3.0), -1/np.sqrt(3.0),  2/np.sqrt(3.0)]), y, rtol=1e-3)


def test_set_nodes_N2():
    x, y = set_nodes_in_equilateral_triangle(2)
    assert np.allclose(
        np.array([-1.0, 0.0, 1.0, -0.5, 0.5,  0.0]), x, rtol=1e-3)
    assert np.allclose(
        np.array(
            [-1/np.sqrt(3.0), -1/np.sqrt(3.0), -1/np.sqrt(3.0),
             1/2/np.sqrt(3.0), 1/2/np.sqrt(3.0), 2/np.sqrt(3.0)]), y, rtol=1e-3)
    
def test_set_nodes_N3():
    x, y = set_nodes_in_equilateral_triangle(3)
    assert np.allclose(
        np.array([-1.0, 
                  -0.447213595499958, 
                  0.4472135954999578, 
                  1.0, 
                  -0.723606797749979, 
                  -1.487246232888964e-16, 
                  0.7236067977499789, 
                  -0.2763932022500211, 
                  0.2763932022500211, 
                  0.0]), x, rtol=1e-14)
    assert np.allclose(
        np.array([-0.5773502691896258,
                  -0.5773502691896258,
                  -0.5773502691896258,
                  -0.5773502691896258,
                  -0.09862320002592881,
                  -7.715922325969622e-17,
                  -0.09862320002592881,
                  0.6759734692155545,
                  0.6759734692155545,
                  1.154700538379252]), y, rtol=1e-14)


def test_xy_to_rs_N3():
    x = np.array([-1.0, 
                  -0.447213595499958, 
                  0.4472135954999578, 
                  1.0, 
                  -0.723606797749979, 
                  -1.487246232888964e-16, 
                  0.7236067977499789, 
                  -0.2763932022500211, 
                  0.2763932022500211, 
                  0.0])
    y = np.array([-0.5773502691896258,
                  -0.5773502691896258,
                  -0.5773502691896258,
                  -0.5773502691896258,
                  -0.09862320002592881,
                  -7.715922325969622e-17,
                  -0.09862320002592881,
                  0.6759734692155545,
                  0.6759734692155545,
                  1.154700538379252])
    assert np.allclose(
        np.array(
            [
                [-1.0,
                 -0.447213595499958,
                 0.447213595499958, 
                 1.0, 
                 -1.0, 
                 -0.3333333333333334, 
                 0.4472135954999578, 
                 -1.0, 
                 -0.4472135954999578, 
                 1.0],
                [-1.0,
                 -1.0,
                 -1.0, 
                 -1.0, 
                 -0.447213595499958, 
                 -0.3333333333333334, 
                 -0.4472135954999578, 
                  0.4472135954999577, 
                 0.4472135954999578, 
                 1.0]]
        ),
        xy_to_rs(x, y)
    )

def test_xy_to_rs_N3():
    x = np.array([0.0, 0.5, 1.0])
    y = np.array([1.0, 1.5, 2.0])
    assert np.allclose(
        np.array(
            [[-((np.sqrt(3.0)+1.0)/3.0), (1.0-3.0*np.sqrt(3.0))/6.0, (-2.0*np.sqrt(3.0)+2.0)/3.0],
             [(4.0*np.sqrt(3.0)-2.0)/6.0, (6.0*np.sqrt(3.0)-2.0)/6.0, (8.0*np.sqrt(3.0)-2.0)/6.0]]
        ),
        xy_to_rs(x, y)
    )

def test_warp_N1():
    L1 = np.array([0, 0, 1])
    L2 = np.array([1, 0, 0])
    L3 = np.array([0, 1, 0])

    N = 1
    Np = 3
    assert np.allclose(np.zeros(Np), warpFactor(N, L3-L2))
    assert np.allclose(np.zeros(Np), warpFactor(N, L1-L3))
    assert np.allclose(np.zeros(Np), warpFactor(N, L2-L1))


def test_simplex_polynomial():
    a, b = (
        np.array([-1,  0,  1, -1,  1, -1]),
        np.array([-1, -1, -1,  0,  0,  1])
    )
    p11 = simplex_polynomial(a, b, 1, 1)
    p11Ref = np.array(
        [2.1213, 0.0000, -2.1213, -1.5910, 1.5910, 0.0000]
    )

    assert np.allclose(p11, p11Ref, rtol=1e-3)


def test_rs_to_ab():
    r, s = (
        np.array([-1.,
                  -0.447213595499958,
                   0.4472135954999577,
                   1.,
                  -1.,
                  -0.3333333333333334,
                   0.4472135954999578,
                  -0.9999999999999999,
                  -0.4472135954999578,
                  -1.]),

        np.array([-1.,
                  -1.,
                  -1.,
                  -1.,
                  -0.447213595499958,
                  -0.3333333333333334,
                  -0.4472135954999578,
                   0.4472135954999577,
                   0.4472135954999577,
                   1.])
    )

    a, b = rs_to_ab(r, s)

    aRef, bRef = (
        np.array([-1.,
                  -0.4472135954999581,
                   0.4472135954999577,
                   1.,
                  -1.,
                  -3.33066907387547e-16,
                   1.,
                  -0.9999999999999996,
                   0.9999999999999991,
                  -1.]),   

        np.array([-1.,
                  -1.,
                  -1.,
                  -1.,
                  -0.447213595499958,
                  -0.3333333333333334,
                  -0.4472135954999578,
                   0.4472135954999577,
                   0.4472135954999577,
                   1.])
    )

    assert (np.allclose(a, aRef, rtol=1e-3))
    assert (np.allclose(b, bRef, rtol=1e-3))

    
def test_rs_to_ab_T2():
    r, s = (
        np.array([-1,  0,  1, -1, 0, -1]),
        np.array([-1, -1, -1,  0, 0,  1])
    )

    a, b = rs_to_ab(r, s)

    aRef, bRef = (
        np.array([-1,  0,  1, -1,  1, -1]),
        np.array([-1, -1, -1,  0,  0,  1])
    )

    assert (np.all(a == aRef))
    assert (np.all(b == bRef))

def test_jacobi_polynomial():
    a, b = (
        np.array([-1,  0,  1, -1,  1, -1]),
        np.array([-1, -1, -1,  0,  0,  1])
    )
    p11 = simplex_polynomial(a, b, 1, 1)
    p11Ref = np.array(
        [2.1213, 0.0000, -2.1213, -1.5910, 1.5910, 0.0000]
    )

    assert np.allclose(p11, p11Ref, rtol=1e-3)

def test_vandermonde_N2():
    # For N = 2.
    r, s = (
        np.array([-1,  0,  1, -1, 0, -1]),
        np.array([-1, -1, -1,  0, 0,  1])
    )

    V = vandermonde(2, r, s)

    VRef = np.array(
        [[0.7071, -1.0000,  1.2247, -1.7321,  2.1213,  2.7386],
         [0.7071, -1.0000,  1.2247,  0.0000,  0.0000, -1.3693],
         [0.7071, -1.0000,  1.2247,  1.7321, -2.1213,  2.7386],
         [0.7071,  0.5000, -0.6124, -0.8660, -1.5910,  0.6847],
         [0.7071,  0.5000, -0.6124,  0.8660,  1.5910,  0.6847],
         [0.7071,  2.0000,  3.6742,  0.0000,  0.0000,  0.0000]]
    )

    assert np.allclose(V, VRef, rtol=1e-3)


def test_nodes_coordinates():
    m = mesh.readFromGambitFile(TEST_DATA_FOLDER + 'Maxwell2D_K146.neu')

    x, y = nodes_coordinates(2, m)

    assert x.shape == y.shape
    assert x.shape == (6, 146)

    xRef = np.array([-1.0000, -1.0000, -1.0000, -0.9127, -0.9127, -0.8253])
    yRef = np.array([-0.7500, -0.8750, -1.0000, -0.7872, -0.9122, -0.8245])

    assert np.allclose(x[:, 0], xRef, rtol=1e-3)
    assert np.allclose(y[:, 0], yRef, rtol=1e-3)


def test_lift_N1():
    liftMat = lift(1)

    liftRef = np.array(
        [[ 2.5000,  0.5000,  -1.5000,  -1.5000,   2.5000,   0.5000],
         [ 0.5000,  2.5000,   2.5000,   0.5000,  -1.5000,  -1.5000],
         [-1.5000, -1.5000,   0.5000,   2.5000,   0.5000,   2.5000]]
    )
    assert np.allclose(liftMat, liftRef, rtol=1e-3)


def test_gradSimplexP():

    a, b = (
        np.array([-1., 0., 1., -1., 1., -1.]),
        np.array([-1., -1., -1., 0., 0., 1.])
    )

    dmodedr, dmodeds = gradSimplexP(a, b, 1, 1)

    dmodedrRef = np.array(
        [-2.1213, -2.1213, -2.1213, 3.1820, 3.1820, 8.4853]
    )

    dmodedsRef = np.array(
        [-6.3640, -1.0607, 4.2426, -1.0607, 4.2426, 4.2426]
    )

    assert np.allclose(dmodedr, dmodedrRef, rtol=1e-3)
    assert np.allclose(dmodeds, dmodedsRef, rtol=1e-3)

def test_gradSimplexP_T2():

    r, s = (
        np.array([-1.0,-0.44721, 0.44721, 1.0,-1.0    ,-0.33333, 0.44721,-1.0,    -0.44721,-1.0]),
        np.array([-1.0,-1.0    ,-1.0    ,-1.0,-0.44721,-0.33333,-0.44721, 0.44721, 0.44721, 1.0])
    )

    a, b = rs_to_ab(r,s)

    dmodedr_zero, dmodeds_zero = gradSimplexP(a, b, 0, 0)
    dmodedr_one, dmodeds_one = gradSimplexP(a, b, 1, 1)

    dmodedrRef_zero = np.zeros(10)

    dmodedsRef_zero = np.zeros(10)

    dmodedrRef_one = np.array(
        [ -2.121320343559643, 
          -2.121320343559643, 
          -2.121320343559643,
          -2.121320343559643,  
           0.810272270213179,  
           1.414213562373095,  
           0.810272270213180,  
           5.553688760465747,   
           5.553688760465747,  
           8.485281374238571])

    dmodedsRef_one = np.array(
        [ -6.363961030678928, 
          -3.432368416906107, 
           1.311048073346462,
           4.242640687119286,  
          -3.432368416906107,  
           0.707106781186546,  
           4.242640687119286,  
           1.311048073346462,   
           4.242640687119285,  
           4.242640687119285])
    
    assert np.allclose(dmodedr_zero, dmodedrRef_zero, rtol=1e-3)
    assert np.allclose(dmodeds_zero, dmodedsRef_zero, rtol=1e-3)
    assert np.allclose(dmodedr_one, dmodedrRef_one, rtol=1e-3)
    assert np.allclose(dmodeds_one, dmodedsRef_one, rtol=1e-3)

def test_gradSimplexP_T3():

    r, s = (
        np.array([-1.0,-0.44721, 0.44721, 1.0,-1.0    ,-0.33333, 0.44721,-1.0,    -0.44721,-1.0]),
        np.array([-1.0,-1.0    ,-1.0    ,-1.0,-0.44721,-0.33333,-0.44721, 0.44721, 0.44721, 1.0])
    )

    a, b = rs_to_ab(r,s)

    dmodedr, dmodeds = gradSimplexP(a, b, 3, 0)

    dmodedrRef = np.array([ 
          2.244994432064365e+01, 
         -9.024596992614826e-05, 
         -9.024596992293053e-05,
          2.244994432064365e+01,  
          1.175488504681664e+01,  
         -2.494425784972035e+00,  
          1.175488504681664e+01,  
          1.715045447181586e+00,   
          1.715045447181586e+00,  
                            0.0])

    dmodedsRef = np.array(
        [  5.612486080160915e+00, 
          -2.509980079602225e+00, 
           2.509980079602221e+00,
           1.683745824048273e+01,  
           2.938735863849390e+00,  
          -1.247219128924648e+00,  
           8.816207591548157e+00,  
           4.287557842471603e-01,   
           1.286267352741480e+00,  
                             0.0])
    
    assert np.allclose(dmodedr, dmodedrRef, rtol=1e-3)
    assert np.allclose(dmodeds, dmodedsRef, rtol=1e-3)


def test_gradVandermonde_N1():

    r, s = (
        np.array([-1., 1., -1.]),
        np.array([-1., -1., 1.])
    )

    V2Dr, V2Ds = gradVandermonde(1, r, s)

    V2DrExp = np.array([
        [0., 0., 1.7321],
        [0., 0., 1.7321],
        [0., 0., 1.7321]]
    )

    V2DsExp = np.array([
        [0., 1.5000, 0.8660],
        [0., 1.5000, 0.8660],
        [0., 1.5000, 0.8660]]
    )

    assert np.allclose(V2Dr, V2DrExp, rtol=1e-3)
    assert np.allclose(V2Ds, V2DsExp, rtol=1e-3)

def test_gradVandermonde_N2():

    r, s = (
        np.array([-1., 0., 1., -1., 0., -1.]),
        np.array([-1., -1., -1., 0., 0., 1.])
    )

    Vr, Vs = gradVandermonde(2, r, s)

    VrExp = np.array([
        [0.0, 0.0, 0.0, 1.7321, -2.1213, -8.2158],
        [0.0, 0.0, 0.0, 1.7321, -2.1213,    0.0],
        [0.0, 0.0, 0.0, 1.7321, -2.1213, 8.2158],
        [0.0, 0.0, 0.0, 1.7321, 3.1820, -4.1079],
        [0.0, 0.0, 0.0, 1.7321, 3.1820, 4.1079],
        [0.0, 0.0, 0.0, 1.7321, 8.4853,    0.0]]
    )

    VsExp = np.array([
        [0.0, 1.5000, -4.8990, 0.8660, -6.3640, -2.7386],
        [0.0, 1.5000, -4.8990, 0.8660, -1.0607, 1.3693],
        [0.0, 1.5000, -4.8990, 0.8660, 4.2426, 5.4772],
        [0.0, 1.5000, 1.2247, 0.8660, -1.0607, -1.3693],
        [0.0, 1.5000, 1.2247, 0.8660, 4.2426, 2.7386],
        [0.0, 1.5000, 7.3485, 0.8660, 4.2426,    0.0]]
    )

    assert np.allclose(Vr, VrExp, rtol=1e-4)
    assert np.allclose(Vs, VsExp, rtol=1e-4)

def test_gradVandermonde_N3():

    r, s = (
        np.array([-1.,
                  -0.447213595499958,
                   0.4472135954999577,
                   1.,
                  -1.,
                  -0.3333333333333334,
                   0.4472135954999578,
                  -0.9999999999999999,
                  -0.4472135954999578,
                  -1.]),

        np.array([-1.,
                  -1.,
                  -1.,
                  -1.,
                  -0.447213595499958,
                  -0.3333333333333334,
                  -0.4472135954999578,
                   0.4472135954999577,
                   0.4472135954999577,
                   1.])
    )

    Vr, Vs = gradVandermonde(3, r, s)

    VrExp = np.array([
        [0.0, 0.0, 0.0, 0.0, 1.732050807568878,	-2.121320343559643,	2.449489742783178 ,-8.215838362577491	  , 9.486832980505138	 , 22.44994432064365    ],
        [0.0, 0.0, 0.0, 0.0, 1.732050807568878,	-2.121320343559643,	2.449489742783178 ,-3.674234614174768	  , 4.242640687119287	 , 4.022165030534275e-15],
        [0.0, 0.0, 0.0, 0.0, 1.732050807568878,	-2.121320343559643,	2.449489742783178 , 3.674234614174764	  ,-4.242640687119282	 ,-7.239897054961693e-15],
        [0.0, 0.0, 0.0, 0.0, 1.732050807568878,	-2.121320343559643,	2.449489742783178 , 8.215838362577491	  ,-9.486832980505138	 , 22.44994432064365    ],
        [0.0, 0.0, 0.0, 0.0, 1.732050807568878,	0.8102722702131788,-1.745166351928364 ,-5.945036488376131	  ,-6.41682933889498	 , 11.75494345539755    ],
        [0.0, 0.0, 0.0, 0.0, 1.732050807568878,	1.414213562373095 ,-1.632993161855452 ,-1.824282583346435e-15 ,-2.808666774861361e-15,-2.494438257849295    ],
        [0.0, 0.0, 0.0, 0.0, 1.732050807568878,	0.8102722702131804,-1.745166351928364 ,	5.945036488376129	  , 6.416829338894984    , 11.75494345539755    ],
        [0.0, 0.0, 0.0, 0.0, 1.732050807568878,	5.553688760465747 , 8.113839683164619 ,-2.270801874201362	  ,-10.65947002601427    , 1.715023136988642    ],
        [0.0, 0.0, 0.0, 0.0, 1.732050807568878,	5.553688760465747 , 8.11383968316462  ,	2.270801874201362	  , 10.65947002601426	 , 1.715023136988639    ],
        [0.0, 0.0, 0.0, 0.0, 1.732050807568878,	8.485281374238571 , 24.49489742783178 ,	0.0	                  , 0.0	                 , 0.0                  ]]
    )

    VsExp = np.array([
        [0,	1.5, -4.898979485566357	, 10.60660171779821	    ,0.8660254037844386, -6.363961030678928, 15.92168332809066	, -2.738612787525831  ,14.23024947075771	,5.612486080160915 ],
        [0,	1.5, -4.898979485566357	, 10.60660171779821	    ,0.8660254037844386, -3.432368416906107, 7.797415561453585	, -0.4678109133244689 ,-1.67341284864241	,-2.509980079602225],
        [0,	1.5, -4.898979485566357	, 10.60660171779821	    ,0.8660254037844389, 1.311048073346462,  -5.3479258186704	, 3.206423700850298	  ,-5.9160535357617	    ,2.509980079602221 ],
        [0,	1.5, -4.898979485566357	, 10.60660171779821	    ,0.8660254037844389, 4.242640687119286,  -13.47219358530748	, 5.47722557505166	  ,4.743416490252574	,16.83745824048273 ],
        [0,	1.5, -1.513867916134242	, -1.311048073346462	,0.8660254037844386, -3.432368416906107, -0.5256355222729966, -1.98167882945871   ,3.656322164364723	,2.93873586384939  ],
        [0,	1.5, -0.8164965809277268, -2.357022603955158	,0.8660254037844388, 0.7071067811865462, -0.8164965809277267, 0.9128709291752759  ,-1.054092553389462	,-1.247219128924648],
        [0,	1.5, -1.513867916134241	, -1.311048073346465	,0.8660254037844389, 4.242640687119286,  -1.219530829655363	, 3.963357658917419   ,10.0731515032597	    ,8.816207591548157 ],
        [0,	1.5, 3.963357658917418	, 3.432368416906099	    ,0.8660254037844386, 1.311048073346462,  -2.1688031947885	, -0.7569339580671209 ,-2.707638866314207	,0.4287557842471603],
        [0,	1.5, 3.963357658917418	, 3.432368416906099	    ,0.8660254037844389, 4.242640687119285,   10.28264287795312	, 1.513867916134241	  ,7.951831159700053	,1.28626735274148  ],
        [0,	1.5, 7.348469228349535	, 21.21320343559643	    ,0.8660254037844386, 4.242640687119285,   12.24744871391589	, 0.0	              ,0.0	                ,0.0               ]]
    )

    assert np.allclose(Vr, VrExp, rtol=1e-3)
    assert np.allclose(Vs, VsExp, rtol=1e-3)

def test_derivative_N1():

    r, s = (
        np.array([-1., 1., -1.]),
        np.array([-1., -1., 1.])
    )

    [Dr, Ds] = derivateMatrix(1, r, s)

    DrExp = np.array([
        [-5.0e-01, 5.0e-01,   0.],
        [-5.0e-01, 5.0e-01,   0.],
        [-5.0e-01, 5.0e-01,   0.]]
    )

    DsExp = np.array([ 
        [-0.5, 0.0, 0.5],
        [-0.5, 0.0, 0.5],
        [-0.5, 0.0, 0.5]]
    )

def test_derivative_N2():

    r, s = (
        np.array([-1., 0., 1., -1., 0., -1.]),
        np.array([-1., -1., -1., 0., 0., 1.])
    )

    [Dr, Ds] = derivateMatrix(2, r, s)

    DrExp = np.array([
        [-1.5000, 2.0000, -0.5000, -0.0000, 0.0000, 0.0000],
        [-0.5000, 0.0000,  0.5000, -0.0000, 0.0000, 0.0000],
        [ 0.5000, 2.0000,  1.5000, -0.0000, 0.0000, 0.0000],
        [-0.5000, 1.0000, -0.5000, -1.0000, 1.0000, 0.0000],
        [ 0.5000, 1.0000,  0.5000, -1.0000, 1.0000, 0.0000],
        [ 0.5000, 0.0000, -0.5000, -2.0000, 2.0000, 0.0000]]
    )

    DsExp = np.array([ 
        [-1.5000,  0.0000,  0.0000,  2.0000, -0.0000, -0.5000],
        [-0.5000, -1.0000,  0.0000,  1.0000,  1.0000, -0.5000],
        [ 0.5000, -2.0000, -0.0000, -0.0000,  2.0000, -0.5000],
        [-0.5000, -0.0000,  0.0000, -0.0000, -0.0000,  0.5000],
        [ 0.5000, -1.0000,  0.0000, -1.0000,  1.0000,  0.5000],
        [ 0.5000, -0.0000,  0.0000, -2.0000, -0.0000,  1.5000]]
    )


def test_geometric_factors():
    N = 1
    x = np.array([[-1.000], [-1.000], [-0.1640]])
    y = np.array([[ 0.000], [-1.000], [-0.1640]])
    r, s = xy_to_rs(*set_nodes_in_equilateral_triangle(N))
    Dr, Ds = derivateMatrix(N, r, s)

    rx, sx, ry, sy, J = geometricFactors(x, y, Dr, Ds)

    assert np.allclose(rx, np.array([[-0.3923], [-0.3923], [-0.3923]]), rtol=1e-3)
    assert np.allclose(sx, np.array([[ 2.3923], [ 2.3923], [ 2.3923]]), rtol=1e-3)
    assert np.allclose(ry, np.array([[-2.0000], [-2.0000], [-2.0000]]), rtol=1e-3)
    assert np.allclose(sy, np.array([[ 0.0000], [ 0.0000], [ 0.0000]]), rtol=1e-3)
    assert np.allclose( J, np.array([[ 0.2090], [ 0.2090], [ 0.2090]]), rtol=1e-3)
    

def test_normals_two_triangles():   

    m = readFromGambitFile(TEST_DATA_FOLDER + 'Maxwell2Triang.neu')
    N = 1
    x, y = nodes_coordinates(N, m)
    r, s = xy_to_rs(*set_nodes_in_equilateral_triangle(N))
    Dr, Ds = derivateMatrix(N, r, s)
    nx, ny, sJ = normals(x, y, Dr, Ds, N)
    

    nxExp = np.array([[-1., -1.,  0.707,  0.707, 0., 0.],[-0.707, -0.707,  0.,  0., 1., 1.]])
    nyExp = np.array([[ 0.,  0., -0.707, -0.707, 1., 1.],[ 0.707,  0.707, -1., -1., 0., 0.]])
    
    # With K=146 and N=2, we have size=(9,146) normals' array, we will considere the first and the end column
    assert np.allclose(nxExp.transpose(), nx, rtol = 1e-3) 
    assert np.allclose(nyExp.transpose(), ny, rtol = 1e-3)

def test_normals_eight_triangles():   

    m = readFromGambitFile(TEST_DATA_FOLDER + 'Maxwell2D_K8.neu')
    N = 3
    x, y = nodes_coordinates(N, m)
    r, s = xy_to_rs(*set_nodes_in_equilateral_triangle(N))
    Dr, Ds = derivateMatrix(N, r, s)
    nx, ny, sJ = normals(x, y, Dr, Ds, N)
    

    nxExp = np.array([
        [-1.0	    ,-0.70711	,-8.0509e-16    ,-8.0509e-16	,1.0	        ,-0.70711	,0.70711	,0.70711],
        [-1.0	    ,-0.70711	,4.893e-16	    ,4.893e-16	    ,1.0	        ,-0.70711	,0.70711	,0.70711],
        [-1.0  	    ,-0.70711	,-3.4312e-16    ,-3.4312e-16	,1.0	        ,-0.70711	,0.70711 	,0.70711],
        [-1.0	    ,-0.70711	,-6.9407e-16    ,-6.9407e-16	,1.0	        ,-0.70711	,0.70711    ,0.70711],
        [0.70711	,3.6637e-15	,-1.0           ,-0.70711	    ,-0.70711	    ,-0.19247	,-0.99022	,-0.1395],
        [0.70711	,-2.8866e-15,-1.0           ,-0.70711	    ,-0.70711	    ,-0.19247	,-0.99022	,-0.1395],
        [0.70711	,2.8866e-15	,-1.0           ,-0.70711	    ,-0.70711	    ,-0.19247	,-0.99022	,-0.1395],
        [0.70711	,4.2188e-15	,-1.0           ,-0.70711	    ,-0.70711	    ,-0.19247	,-0.99022	,-0.1395],
        [0.19247	,0.9813	    ,0.70711	    ,1.0	        ,1.4433e-15	    ,0.99022	,0.1395	    ,-0.9813],
        [0.19247	,0.9813	    ,0.70711	    ,1.0	        ,6.6613e-16	    ,0.99022    ,0.1395	    ,-0.9813],
        [0.19247	,0.9813	    ,0.70711	    ,1.0	        ,-1.1102e-15	,0.99022	,0.1395	    ,-0.9813],
        [0.19247	,0.9813  	,0.70711	    ,1.0	        ,-3.5527e-15	,0.99022	,0.1395	    ,-0.9813]
    ])
    nyExp = np.array([
        [-9.0695e-16	,0.70711	,1.0            ,1.0            ,8.0509e-16	    ,0.70711	,0.70711	,-0.70711],
        [4.7322e-16	    ,0.70711	,1.0            ,1.0            ,-4.893e-16	    ,0.70711	,0.70711	,-0.70711],
        [-2.8309e-16	,0.70711 	,1.0            ,1.0            ,3.4312e-16	    ,0.70711	,0.70711	,-0.70711],
        [-6.7456e-16	,0.70711	,1.0            ,1.0            ,6.9407e-16	    ,0.70711	,0.70711	,-0.70711],
        [-0.70711	    ,-1.0       ,-4.5519e-15	,-0.70711	    ,0.70711	    ,-0.9813	,0.1395 	,0.99022 ],
        [-0.70711	    ,-1.0       ,2.9976e-15	    ,-0.70711	    ,0.70711	    ,-0.9813	,0.1395 	,0.99022 ],
        [-0.70711	    ,-1.0       ,-2.4425e-15	,-0.70711	    ,0.70711	    ,-0.9813	,0.1395	    ,0.99022 ],
        [-0.70711	    ,-1.0       ,-3.3307e-15	,-0.70711	    ,0.70711	    ,-0.9813	,0.1395	    ,0.99022 ],
        [0.9813	        ,0.19247	,-0.70711	    ,1.4433e-15	    ,-1.0           ,-0.1395    ,-0.99022   ,-0.19247],
        [0.9813	        ,0.19247    ,-0.70711	    ,6.6613e-16	    ,-1.0           ,-0.1395	,-0.99022   ,-0.19247],
        [0.9813	        ,0.19247    ,-0.70711	    ,-1.1102e-15	,-1.0           ,-0.1395	,-0.99022   ,-0.19247],
        [0.9813	        ,0.19247    ,-0.70711	    ,-3.5527e-15	,-1.0           ,-0.1395    ,-0.99022   ,-0.19247]
    ]),
    
    assert np.allclose(nxExp, nx, rtol = 1e-3) 
    assert np.allclose(nyExp, ny, rtol = 1e-3)



def test_grad():
    N = 1
    mesh = readFromGambitFile(TEST_DATA_FOLDER + 'Maxwell2Triang.neu')

    x, y = nodes_coordinates(N,mesh)
    r, s = xy_to_rs(*set_nodes_in_equilateral_triangle(N))
    Dr, Ds = derivateMatrix(N, r, s)
    
    Ez = np.array([[1., 2.],[3., 4.], [5., 6.]])
    rx, sx, ry, sy, _ = geometricFactors(x, y, Dr, Ds)

    Ezx, Ezy = grad(Dr, Ds, Ez, rx, sx, ry, sy)

    EzxExp = np.array([[ 4.,  2.],
                       [ 4.,  2.], 
                       [ 4.,  2.]])
    
    EzyExp = np.array([[-2., -4.],
                       [-2., -4.], 
                       [-2., -4.]])
    
    assert np.allclose(EzxExp, Ezx, rtol = 1e-3)
    assert np.allclose(EzyExp, Ezy, rtol = 1e-3)

def test_curl():
    N = 1
    mesh = readFromGambitFile(TEST_DATA_FOLDER + 'Maxwell2Triang.neu')
    x, y = nodes_coordinates(N, mesh)
    r, s = xy_to_rs(*set_nodes_in_equilateral_triangle(N))
    Dr, Ds = derivateMatrix(N, r, s)
    
    Hx = np.array([[ 1., 20.],[ 5., 8.], [300., 40.]])
    Hy = np.array([[30.,  2.],[50., 3.], [ 10.,  4.]])

    rx, sx, ry, sy, _ = geometricFactors(x, y, Dr, Ds)
    CuZ = curl(Dr, Ds, Hx, Hy, rx, sx, ry, sy)

    CuZExp = np.array([ [ -16., 21.],
                        [ -16., 21.], 
                        [ -16., 21.]])
    
    assert np.allclose(CuZExp, CuZ, rtol = 1e-3)
