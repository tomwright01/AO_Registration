from nose.tools import *
import AoRegistration.AoRecording as AoRecording
import AoRegistration.StackTools as stackTools
import numpy as np

vid = AoRecording.AoRecording(filepath='data/sample.avi')
vid.load_video()

def setup():
    print "SETUP!"
    

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"


def test_load_video():
    vid = AoRecording.AoRecording(filepath='data/sample.avi')
    vid.load_video(cropInterlace=False)
    assert_equal(vid.nframes,32)
    assert_equal(vid.frameheight,1024)
    assert_equal(vid.framewidth,1000)
    assert_equal(vid.data.shape,(32,1024,1000))
    
@with_setup(setup)        
def test_set_mask():
    #vid = AoRecording.AoRecording(filepath='data/sample.avi')
    testMask = np.zeros((1024,1000),dtype=np.bool)
    testMask[250:255,50:55] = 1
    
    vid.set_mask(roi=[(50,250),(55,255)])
    assert(np.array_equal(vid.mask, testMask))

@with_setup(setup)        
@raises(AssertionError)
def check_set_mask2(arg):
    #vid = AoRecording.AoRecording(filepath='data/sample.avi')
    x1,y1 = arg[0]
    x2,y2 = arg[1]
    
    vid.set_mask(roi=[(x1,y1),(x2,y2)])
    
def test_set_mask2():
    # all these params should raise an AssertionError
    invalid_args = [[(-5,10),(10,10)],
                    [(5,10),(-5,10)],
                    [(5,-5),(5,-5)],
                    [(5,-5),(5,1500)]]
    for arg in invalid_args:
        yield(check_set_mask2,arg)
        
def test_quadrant_detect():
    x = np.array(range(144),dtype=np.float).reshape((12,12),order = 'F')
    x[5,5] = 144
    x=x/x.sum()    
    target = (5.7136351459951777, 7.6843718079673131)
    result = stackTools.quadrant_detect(x)
    assert np.allclose(result, target),'myerror'