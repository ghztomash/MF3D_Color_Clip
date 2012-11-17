# http://tomashg.com
# ghz.tomash@gmail.com
# Color clips script for MIDI Fighter 3D from DJ TECH TOOLS

import Live
import math
import time # We will be using time functions for time-stamping our log file outputs
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent 
from _Framework.DeviceComponent import DeviceComponent
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.SessionComponent import SessionComponent
from SpecialSessionComponent import SpecialSessionComponent
from SpecialZoomingComponent import SpecialZoomingComponent
from ConfigurableButtonElement import ConfigurableButtonElement
from Settings import *
from Constants import *

class MF3D_Color_Clip(ControlSurface):
    __doc__ = " Script for Mad Zach's Weekly soundpacks "

    _active_instances = []

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= MIDI Fighter Mad Zach Soundpack log opened =--------------") # Writes message into Live's main log file. This is a ControlSurface method.
        self.set_suppress_rebuild_requests(True)
        self._session = None
        self._session_zoom = None
        self._last_tr_off = 0
        self._last_sc_off = 1
        self._setup_session_control()
        self.set_suppress_rebuild_requests(False)

    def disconnect(self):
        self._session = None
        self._session_zoom = None
        self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= MIDI Fighter Mad Zach Soundpack log closed =--------------") # Writes message into Live's main log file. This is a ControlSurface method.
        ControlSurface.disconnect(self)

    def _setup_session_control(self):
        is_momentary = True
        self._device = DeviceComponent()
        self._device.name = 'Device_Component'
        self._session = SpecialSessionComponent(4, 4)
        self._session.name = 'Session_Control'
        self._session.set_track_bank_buttons(self._set_button(BUTTONCHANNEL+1, SESSIONRIGHT),self._set_button(BUTTONCHANNEL+1, SESSIONLEFT))
        self._session.set_scene_bank_buttons(self._set_button(BUTTONCHANNEL+1, SESSIONDOWN),self._set_button(BUTTONCHANNEL+1, SESSIONUP))
        self._session_zoom = SpecialZoomingComponent(self._session)
        self._session_zoom.name = 'Session_Overview'
        self._session_zoom.set_nav_buttons(self._set_button(BUTTONCHANNEL+1, ZOOMUP), self._set_button(BUTTONCHANNEL+1, ZOOMDOWN), self._set_button(BUTTONCHANNEL+1, ZOOMLEFT), self._set_button(BUTTONCHANNEL+1, ZOOMRIGHT))
        tracks = self.getslots() #get clip slots to access clip colors
        for scene_index in range(4):
            scene_off=self._session._scene_offset
            scene = self._session.scene(scene_index+scene_off)
            scene.name = 'Scene_' + str(scene_index+scene_off)
            button_row = []
            for track_index in range(4):
                button = self._set_button(BUTTONCHANNEL, CLIPNOTEMAP[scene_index][track_index], GREEN, OFF)
                button_row.append(button)
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = str(track_index) + '_Clip_Slot_' + str(scene_index+scene_off)
                clip_slot.set_launch_button(button)
                c = tracks[track_index][scene_index+scene_off] #get clip for color
                clip_slot.set_stopped_value(LOWYELLOW)
                if c.clip != None:
                    cval=self._get_MF3D_color(self.int_to_rgb(c.clip.color))
                    self.log_message("Clip:  tr: " + str(track_index) + " clip: " + str(scene_index+scene_off) + " has color: " + str(self.int_to_rgb(c.clip.color)) + " va " + str(cval))
                    clip_slot.set_stopped_value(cval)
##                clip_slot.set_triggered_to_launch_value(1)
                clip_slot.set_triggered_to_play_value(PLAYTRIG_COL)
                clip_slot.set_started_value(TRIGD_COL)
                clip_slot.set_triggered_to_record_value(RECTRIG_COL)
                clip_slot.set_recording_value(RECD_COL)

    def int_to_rgb(self,rgbint):
        return (rgbint/256/256%256, rgbint/256%256,rgbint%256)

    def getslots(self):
        tracks = self.song().visible_tracks

        clipSlots = []
        for track in tracks:
            clipSlots.append(track.clip_slots)
        return clipSlots

    def _set_button(self,_channel,_note,_on_color=118,_off_color=0):
        _button=None;
        if not _note is -1:
          _button = ConfigurableButtonElement(True, MESSAGETYPE, _channel, _note,_on_color,_off_color)
        return _button

    def _set_colors(self, scene_dir):
        tracks = self.getslots() #get clip slots to access clip colors
        scene_off=self._session.scene_offset()
        track_off=self._session.track_offset()
        for scene_index in range(4):
            sc=scene_index
            scene = self._session.scene(sc)
            self.log_message("scene offset + index " + str(scene_index))
            scene.name = 'Scene_' + str(scene_index)
            button_row = []
            for track_index in range(4):
                #button = self._set_button(BUTTONCHANNEL, CLIPNOTEMAP[scene_index][track_index], GREEN, OFF)
                #button_row.append(button)
                tr=track_index
                clip_slot = scene.clip_slot(tr)
                clip_slot.name = str(track_index) + '_Clip_Slot_' + str(scene_index)
                #clip_slot.set_launch_button(button)
                c = tracks[track_index][scene_index+scene_off+scene_dir] #get clip for color
                clip_slot.set_stopped_value(LOWYELLOW)
                if c.clip != None:
                    cval=self._get_MF3D_color(self.int_to_rgb(c.clip.color))
                    clip_slot.set_stopped_value(cval)
                    self.log_message("Clip:  tr: " + str(track_index) + " clip: " + str(scene_index) + " has color: " + str(self.int_to_rgb(c.clip.color)) + " va " + str(cval))

    def update_display(self):
        ControlSurface.update_display(self)
        scene_off=self._session.scene_offset()
        track_off=self._session.track_offset()
        if (scene_off>self._last_sc_off):
            self.log_message("vooce"+ str(self._session._track_offset)+ " " +str(self._session._scene_offset))
            self._set_colors(1)
            self._last_tr_off = track_off
            self._last_sc_off = scene_off
        if (scene_off<self._last_sc_off):
            self.log_message("vooce"+ str(self._session._track_offset)+ " " +str(self._session._scene_offset))
            self._set_colors(-1)
            self._last_tr_off = track_off
            self._last_sc_off = scene_off

    def _get_MF3D_color(self, colors):
        red = colors[0]
        green = colors[1]
        blue = colors[2]
        color_table=((255,0,0,RED),(125,0,0,LOWRED),(255,127,0,ORANGE),(127,64,0,LOWORANGE),
                     (255,255,0,YELLOW),(127,127,0,LOWYELLOW),(127,255,0,CHARTREUSSE),(64,127,0,LOWCHARTREUSSE),
                     (0,255,0,GREEN),(0,127,0,LOWGREEN),(0,255,255,CYAN),(0,127,127,LOWCYAN),
                     (0,0,255,BLUE),(0,0,127,LOWBLUE),(0,255,127,PURPLE),(0,127,64,LOWPURPLE),
                     (0,255,255,PINK),(0,127,127,LOWPINK),(255,255,255,WHITE))
        min_dist=9999999
        color_node=(0,0,0,119)
        for index in range(len(color_table)):
             if (min_dist>self._get_distance(colors,color_table[index])):
                min_dist=self._get_distance(colors,color_table[index])
                #self.log_message("colors " +  str(color_node) + " and " + str(color_table[index]))
                color_node=color_table[index]
        #self.log_message("red " + str(red) + " green " + str(green) + " blue " + str(blue) + " distance to" + str(color_node[3]) + " :: " + str(self._get_distance(colors,color_node))) 
        return color_node[3]

    def _get_distance(self,color1,color2):
        r1=color1[0]
        g1=color1[1]
        b1=color1[2]
        r2=color2[0]
        g2=color2[1]
        b2=color2[2]
        #self.log_message("got " + str(color1) + " and " + str(color2))
        return (abs((r1-r2))+abs((g1-g2))+abs((b1-b2)))